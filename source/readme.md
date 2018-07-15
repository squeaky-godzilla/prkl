# PRKL API source code

## Code structure

API is written in Python 2.7, using fairly standard libraries.
Query functions are defined outside of the API routes. I found this somewhat useful to decouple the exceptions handling (data processing errors vs parameters inputs).

### Routes

- '/songs/load/', POST
  - takes parameter 'myfile' for loads into the MongoDB
  - file is saved as 'upload.json' in ./uploads

- '/songs/purge/', POST
  - post to this endpoint to completely drop 'ratings' and 'songs'
  - purrrrrge!

- '/songs/avg/difficulty/', GET, parameters: level (integer)
  - Takes an optional parameter "level" to select only songs from a specific level.
  - Returns the average difficulty for all songs.

- '/songs', GET, parameters: offset (integer), per_page (integer)
  - Returns a list of songs with some details on them
  - If you wish to retrieve per pages, set the per_page param (you can also set the offset if you wish)

- '/songs/search', GET, parameters: message (string)
  - Takes in parameter a 'message' string to search.
  - Return a list of songs. The search should take into account song's artist and title. The search should be case insensitive.

- '/songs/rating', POST, parameters: song_id (MongoDB object ID), rating (integer)
  - This call adds a rating to the song. Ratings should be between 1 and 5.

- '/songs/avg/rating/<song_id>', GET
  - Returns the average, the lowest and the highest rating of the given song id.


### Logger

To log errors and events, I've implemented a small function called "logger". This outputs the relevant messages to stdout. This is because this part of the solution is primarily intended to run on a container.

Containerised solutions are designed for graceful failure, so on a container fail, you could lose relevant log files. Therefore, it is better to pass the messages and logs to stdout or stderr.
