import json
import sqlite3

# This program shouldn't be run more than once !
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

# artistSummary table
summary = {}
cursor.execute('''
CREATE TABLE IF NOT EXISTS artistSummary (
    artistId INTEGER UNIQUE,
    totalMsPlayed INTEGER
    )
''')
cursor.execute('SELECT * FROM streamingHistory')
streamingHistory = cursor.fetchall()
for item in streamingHistory:
    endTime = item[0]
    trackId = item[1]
    msPlayed = item[2]
    if artistId not in summary.keys():
        summary[artistId] =  msPlayed
    else :
        summary[artistId] += msPlayed
    songsArtistsCursor.execute("SELECT artistId from Songs WHERE id IS ?", (trackId, ))
    artistId = songsArtistsCursor.fetchone()[0]

for artistId, totalMsPlayed in summary.items():
    cursor.execute("INSERT OR IGNORE INTO artistSummary (artistId, totalMsPlayed) VALUES (?, ?)", (artistId, totalMsPlayed))
connection.commit()

# songSummary table
summary = {}
cursor.execute('''
CREATE TABLE IF NOT EXISTS songSummary (
    trackId INTEGER UNIQUE,
    totalMsPlayed INTEGER
    )
''')
cursor.execute('SELECT * FROM streamingHistory')
streamingHistory = cursor.fetchall()
for item in streamingHistory:
    endTime = item[0]
    trackId = item[1]
    msPlayed = item[2]
    songsArtistsCursor.execute("SELECT artistId from Songs WHERE id IS ?", (trackId, ))
    artistId = songsArtistsCursor.fetchone()[0]
    if trackId not in summary.keys():
        summary[trackId] =  msPlayed
    else :
        summary[trackId] += msPlayed

for trackId, totalMsPlayed in summary.items():
    cursor.execute("INSERT OR IGNORE INTO songSummary (trackId, totalMsPlayed) VALUES (?, ?)", (trackId, totalMsPlayed))
connection.commit()
