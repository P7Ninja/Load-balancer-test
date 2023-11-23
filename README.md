# Web Application

This is the repo for the meal web application for our P7 project, it includes all submodules for the application. 

## Development

To develop on the application do the steps in the setup section and then develop on each submodule and commit from there to test the application use docker-compose with the `docker-compose.yaml` file. 



run the create_data.py script to create test data, remember to `pip install -r requirements.txt`:
```sh
python ./scripts/create_data.py -o ./database/data.sql
```

To build and start docker in the terminal with output:
```sh
docker compose -f docker-compose.yaml build
docker compose -f docker-compose.yaml up
```

Start up in background
```sh
docker compose -f docker-compose.yaml up -d
```

shutdown compose:
```sh
docker compose down
```

### Setup
To pull all the submodules use:
```sh
git submodule update --init --recursive
```

To update all submodules to latest commit:
```sh
git submodule update --recursive --remote
```

fetch commits:
```sh
git submodule update --recursive --remote --fetch
```

## Deployment with Docker Swarm
To deploy the server use the `Docker-Swarm-Example.yaml` to create your own.
use the name `Docker-Swarm.yaml` as this file name is ignored so that secrets in the file wont be pushed to the repo. 

remember to create a SSL certificate if using https.

