import yaml
import requests
import argparse
import time 
from urllib.parse import urlparse
    
class HealthChecker():
    '''
        HealthChecker creates an object which runs health checks for HTTP/HTTPS endpoints at a fixed interval.
        -----------
        Parameters:
        -----------
        configPath : str
            The filepath to the YAML config file consisting of the payload information
        delay: int
            Time in seconds to wait after a runHealthCheck() call
        -----------
        Methods:
        -----------
        parseConfig() => list[dict]
            Reads and parses config file, returns unformatted requests
        
        createRequests(unformattedRequests) => list[dict]
            Formats request payloads and fills in missing values
        
        runHealthCheck() => None
            Sends requests, captures response, calulates statistics, prints health stats,
            repeats after 'self.delay'
    
    '''
    
    def __init__(self, configPath:str, delay:int=15, latencyThreshold:int=500) -> None:
        self.configPath = configPath
        self.delay = delay
        self.latencyThreshold = latencyThreshold
        self.aggregatedStats = {}
        self.allRequests = []


        if self.configPath:
            unformattedRequests = self.parseConfig()
            if unformattedRequests:
                self.allRequests = self.createRequests(unformattedRequests)
    
    def parseConfig(self) -> 'list[dict]':
        try:
            with open(self.configPath, "r") as stream:
                unformattedRequests = yaml.safe_load(stream)
        except:
            print(f'Invalid config path set: {self.configPath}')
            return None
        return unformattedRequests
    
    def createRequests(self, unformattedRequests) -> 'list[dict]':
        allRequests = []
        for req in unformattedRequests:
            
            headers = req.get('headers', '')
            payload = req.get('body', '')
            method = req.get('method', 'GET')
            url = req.get('url')
            name = req.get('name')
            if name == None or url == None:
                print(f'Missing parameters in {req}')
                print('Skipping invalid request.')
                continue

            formattedRequest = {'headers': headers, 'method': method, 'url': url, 'payload': payload}
            allRequests.append(formattedRequest)
        
        return allRequests
    
    def runHealthCheck(self) -> None:
        if self.allRequests == []: return
        while 1:
            for req in self.allRequests:
                parsed_uri = urlparse(req['url'])
                hostname = '{uri.netloc}'.format(uri=parsed_uri)
                if hostname not in self.aggregatedStats:
                    self.aggregatedStats[hostname] = {'up': 0, 'total': 0}

                response = requests.request(method=req['method'], url=req['url'], params=req['payload'], headers=req['headers'])
                if response.elapsed.total_seconds() * 1000 < self.latencyThreshold and 200 <= response.status_code <= 299:
                    self.aggregatedStats[hostname]['up'] += 1
                self.aggregatedStats[hostname]['total'] += 1
            
            for hostname in self.aggregatedStats:
                ups = self.aggregatedStats[hostname]["up"]
                totals = self.aggregatedStats[hostname]["total"]
                print(f'{hostname} has {round((ups/totals) * 100)}% availability percentage')

            time.sleep(self.delay)

if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="My script")
    parser.add_argument('-p', '--path', type=str, help="YAML config path", required=True)
    parser.add_argument('-d', '--delay', type=int, help="Delay after healthCheck", required=False, default=15)
    parser.add_argument('-l', '--latency', type=str, help="Latency Threshold", required=False, default=500)
    args = parser.parse_args()
    configPath = args.path
    delay = args.delay
    latency = args.latency
    
    obj = HealthChecker(configPath, delay, latency)
    obj.runHealthCheck()