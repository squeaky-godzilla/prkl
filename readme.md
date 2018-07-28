# PRKL - Flask API & MongoDB showcase

## Terve! Welcome!

Welcome to the PRKL!

"./data": This folder contains correct and not-so-correct song data for MongoDB imports

"./docs": This contains AWS solution description and other deployment related bits of information

"./infra": Infrastructure-as-a-code folder for lab deployment of PRKL

"./source": PRKL Flask API source code & tests


*Most of the folders in the repo will contain a relevant readme.md file*


### What's this?

This is a showcase of a Flask API with MongoDB backend. The API has following capabilities:
- load song records from a valid JSON file
- retrieve all records either in one request or in paginated form
- retrieve selected results above specific level with stats aggregation
- regexp powered substring search for "artist" and "title" fields
- add rating to songs
- retrieve stats aggregations for song ratings
- purge all data from the database collections

## How does it work?

### MongoDB
The database "prkl" is divided into two collections - "songs" and "ratings". Ratings are stored per object id from "songs" collection (rating record looks like this - "rating object id": {"song id": something, "rating": 3}).

The interaction between the API and the database is handled by the "pymongo" library.

### Flask API
Flask API (/source/ folder) is structured in following way:
- app.py: the main program, contains query fucntions and route definitions
- /snippets/checks.py: added as external snippets library, currently contains a format checker only
- /tests/: contains API tests for Tavern (Tavern is a neat plugin for pytest, making it possible to specify test cases in YAML)
- /upload: a folder for JSON file upload for the database imports
- prkl-api.conf: Upstart service configuration (for VM based deployments)

### Testing
Test cases are built for Tavern, they are meant to test the possible edge cases - especially of user POST methods on API routes. Since they are written in YAML, they are self explanatory.
