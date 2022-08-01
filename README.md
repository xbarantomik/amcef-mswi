# amcef-mswi

Microservice in Python to moderate Posts

## Getting started
These instructions will cover information for usage of the docker container

## Prerequisities

In order to run this container you'll need docker installed

* [Docker for Windows](https://docs.docker.com/windows/started)

## Usage

Build and run the container (from the root repository)

```shell
docker-compose build
```

```shell
docker-compose up
```
Now, you should see the server running

Run this command in other command line to open the containers command line (`mswi_container` is name of the container)
```shell
docker exec -it mswi_container /bin/bash
```

In there, you'll need to migrate the database
```shell
python manage.py makemigrations ms_api
```
```shell
python manage.py migrate
```

The server should be running with the database migrated

## API Documentation

[API Documentation](https://app.swaggerhub.com/apis/adambarantomik/AMCEF-MSWI/1.0.0#/servers)

## Author

* **Adam Baran-Tomik**