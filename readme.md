# Python Flask API

## Requirements:
- Use python with Flask.
- Use a MongoDB server for storing the data provided in the file "songs.json".
- All routes should return a valid json dictionary.
- Write tests for the API.
- Follow the KISS principle.
- Provide all instructions to do the setup, the easier it is for us to get it running the better.
- Please take into consideration that the number of songs and ratings will grow to millions of documents as well as the number of users using the API.

## List of routes to implement:
- GET /songs
  - Returns a list of songs with some details on them
  - Add possibility to paginate songs.

- GET /songs/avg/difficulty
  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.

- GET /songs/search
  - Takes in parameter a 'message' string to search.
  - Return a list of songs. The search should take into account song's artist and title. The search should be case insensitive.

- POST /songs/rating
  - Takes in parameter a "song_id" and a "rating"
  - This call adds a rating to the song. Ratings should be between 1 and 5.

- GET /songs/avg/rating/<song_id>
  - Returns the average, the lowest and the highest rating of the given song id.

## After developing this Flask API:
- Design a high-level system architecture to support the above.
- If you’re comfortable with AWS, define the AWS components to support the system architecture design.
- Describe what is your strategy for scaling each components of the system. Imagine millions of users and on weekends, the traffic could easily spike to 3-5x the average traffic.
- Think about components that may be required to monitor and maintain the system
- Describe and justify the tooling you would use for development, continuous integration and running the application on prod.
- You can use any diagramming tool you wish (one example could be http://dia-installer.de/). You can also use a pen and paper and take a photo.

## Bonus:
- Putting your work in a git repository is a plus.
