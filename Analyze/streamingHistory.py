import json
import sqlite3

connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()
streamingHistory = json.loads(open("../MySpotifyData/StreamingHistory0.json").read())
songsArtistsConnection = sqlite3.connect("../Databases/songsArtists.sqlite")
songsArtistsCursor = songsArtistsConnection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS streamingHistory
    (
    endTime Date,
    trackId INTEGER,
    msPlayed INTEGER
    )
''')

for song in streamingHistory:
    endTime = song['endTime']
    artistName = song['artistName']
    trackName = song['trackName']
    msPlayed = song['msPlayed']
    songsArtistsCursor.execute("SELECT id from Artists WHERE artistName IS ( ? )", (artistName, ) )
    artistId = songsArtistsCursor.fetchone()[0]
    songsArtistsCursor.execute("SELECT id from Songs WHERE trackName IS ( ? )", (trackName, ) )
    trackId = songsArtistsCursor.fetchone()[0]
    print((endTime, trackId, artistId, msPlayed))
    cursor.execute("INSERT INTO streamingHistory (endTime, trackId, msPlayed) VALUES (?, ?, ?)", (endTime, trackId, msPlayed, ))
    connection.commit()
