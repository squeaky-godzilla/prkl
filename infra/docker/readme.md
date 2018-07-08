# PRKL Docker version

## Installation:

- clone the repo
- install docker and docker-compose
- copy the *"api_functions.py"* from the *"source/"* folder
- go to the "infra/docker" folder
- run docker-compose up
- import the test data from "data/songs.json" file by running `python source/init_data_load.py 10.5.0.6:27017`
- access the API on `localhost:5000/songs/`
