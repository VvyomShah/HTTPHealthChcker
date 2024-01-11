This script provides a simple and configurable health-checking mechanism for HTTP/HTTPS endpoints. It reads configuration details from a YAML file, sends requests to specified URLs, captures responses, calculates statistics, and prints health statistics.
Prerequisites

    Python 3.x

Installation

    Clone the repository or download the script:

    bash

git clone https://github.com/VvyomShah/HTTPHealthChcker/
cd health-checker

Install the required Python packages:

bash

    pip install -r requirements.txt

Usage
Command Line Arguments

    -p or --path: Path to the YAML config file containing payload information (required).
    -d or --delay: Time in seconds to wait after a runHealthCheck() call (optional, default is 15 seconds).
    -l or --latency: Latency threshold in milliseconds, beyond which a request is considered slow (optional, default is 500 milliseconds).

Example

python health_checker.py -p path/to/config.yaml -d 15 -l 500

This command runs the health checker with a custom delay of 30 seconds and a latency threshold of 1000 milliseconds using the specified config file.
Configuration File (YAML)

The YAML config file should have the following structure:

yaml

- name: example_request
  method: GET
  url: https://example.com/api
  headers:
    Content-Type: application/json
  body:
    key1: value1
    key2: value2

- name: another_request
  method: POST
  url: https://example.com/submit
  headers:
    Authorization: Bearer <token>
  body:
    data: "example data"

    name: A unique identifier for the request.
    method: HTTP method (GET, POST, PUT, DELETE, etc.).
    url: The URL to send the request to.
    headers: Optional headers for the request.
    body: Optional request payload.

Running the Health Checker

After configuring the YAML file, run the health checker with the following command:

python health_checker.py -p path/to/config.yaml

The script will continuously send requests to the specified endpoints, calculate availability percentages, and print the results at the specified interval. Press Ctrl + C to stop the health checker.

Feel free to customize the script and the configuration file to suit your specific use case.