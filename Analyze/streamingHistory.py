import json
import sqlite3

connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()
streamingHistory = json.loads(open("../MySpotifyData/StreamingHistory0.json").read())

cursor.execute('''
    CREATE TABLE IF NOT EXISTS streamingHistory
    (
    endTime Date,
    artistName Text,
    trackName Text,
    msPlayed Integer
    )
''')

for song in streamingHistory:
    endTime = song['endTime']
    artistName = song['artistName']
    trackName = song['trackName']
    msPlayed = song['msPlayed']
    cursor.execute("INSERT INTO streamingHistory (endTime, artistName, trackName, msPlayed) VALUES (?, ?, ?, ?)", (endTime, artistName, trackName, msPlayed, ))
    connection.commit()
