# PRKL Docker version

This is probably the fastest and easiest method to deploy. Extensively tested on Linux, tested on MacOSX and somewhat tested on Windows systems. Creates a backend network 'lab_net' where both containers communicate. API port :5000 is forwarded to the localhost address, use localhost address to communicate to the API.

## Installation:

### How this works?
- Run this on your Docker host
- This will build the PRKL Flask API image out of Python 2.7 image
- It will deploy MongoDB image from the repository
- both containers will be connected via lab network using bridge driver

'Dockerfile' for the Flask API frontend container:

```FROM python:2.7
WORKDIR /app
COPY app.py /app
COPY snippets /app
RUN pip install pymongo flask
ENTRYPOINT ["python"]
CMD ["app.py","10.5.0.6:27017"]```

docker-compose.yml for the whole service:

```version: '2'
services:
  prkl_api:
    build: .
    ports:
     - "5000:5000"
    networks:
      lab_net:
        ipv4_address: 10.5.0.5
  mongo:
    image: "mongo:latest"
    networks:
      lab_net:
        ipv4_address: 10.5.0.6

networks:
  lab_net:
    driver: bridge
    ipam:
     config:
       - subnet: 10.5.0.0/16```


### Windows host

- clone the repo
- install docker and docker-compose
- copy the *"app.py"* and the *"snippets/"* folder from the *"source/"* folder to this (/infra/docker/) folder
- go to the "infra/docker" folder
- run `docker-compose up --build`
- import the test data from "data/songs.json" file by POSTing here `curl -F myfile=@../../data/songs.json http://localhost:5000/songs/load/`
- access the API at `http://localhost:5000/songs/`


### Linux or MacOSX host

- clone the repo
- install docker and docker-compose
- go to the '/infra/docker/' folder
- execute `deploy.sh` script
- import the test data from "data/songs.json" file by POSTing here `curl -F myfile=@../../data/songs.json http://localhost:5000/songs/load/`
- access the API at `http://localhost:5000/songs/`


### Notes & troubleshooting

- check if your docker service is running
- check if you don't have a conflicting docker network namespace
