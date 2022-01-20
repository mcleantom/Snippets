# RoutingServer

A REST API to run and get the results of Wind Wings route optimisation with ShipSeat.

## Installation

`pip install --extra-index-url http://pypi.bar.local --trusted-host pypi.bar.local RoutingServer`

## Deployment

The `dev` branch is automatically deployed to our test server. See:

    http://routing_server.bar.local/docs

Deployment is managed from http://jenkins.bar.local and the `Jenkinsfile` in the project root directory.

## Running
To run locally:

`python -m RoutingServer --help`

## Docker
To run in docker you can pull from our docker repo
```
docker pull docker.bar.local:5000/bar_technologies/routingserver:latest
docker run -d --name routingserver --restart unless-stopped \
    -p 5000:80 \
    bar_technologies/routingserver:latest
```
Or you can build and run:
```
docker build -t routingserver .
docker run --name routingserver -d -p 5000:80 routingserver  # expose port 5000 locally
```
## Development
```
conda create --name RoutingServer python==3.8
conda activate RoutingServer
pip install -r requirements.txt
pip install -r requirements_dev.txt
```
### Other Requirements
This project depends on `datamodels` and `mongobase`. Get them from bitbucket or from pypi.bar.local and add them to 
your IDE.

### Black
We use [black](https://github.com/psf/black) to handle code formatting.
```
conda activate RoutingServer
pre-commit install
```
