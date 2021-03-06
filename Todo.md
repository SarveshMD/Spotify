# Project - Visualize Spotify Data

## Resources we have

### ( Ordered by the amount of useful data they contain )

1. Playlist1.json
2. StreamingHistory0.json
3. YourLibrary.json
4. SearchQueries.json
5. Userdata.json
6. Follow.json
7. Inferences.json
8. Identity.json
9. Payments.json

## What we're going to do

1. Analyze and parse the files
    - Analyze Streaming History
    - Analyze Playlists
    - Analyze Library
    - Analyze User Data
    - Analyze Follow Data
    - Create SQLite File with analyzed data
2. Compare things
    - Streaming History
    - Playlists
    - Library
3. Get the results
    - Get the songs ordered by longest time played
    - Get the most frequently played song at a particular time
    - Get the most favorite artist
    - Get the most favorite song

## How do we start

1. We'll create an sqlite file to store our streaming history.
2. We'll create another sqlite file with a table for each playlist and add all the playlists to it.
3. We'll create a sqlite for all songs and artists, it will contain two tables, artists and songs.
