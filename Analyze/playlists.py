import json
import sqlite3

connection = sqlite3.connect("../Databases/playlists.sqlite")
cursor = connection.cursor()
playlists = json.loads(open("../MySpotifyData/Playlist1.json").read())['playlists']

for playlist in playlists:
    name = playlist['name'].replace(" ", "_")
    items = playlist['items']
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {name}
        (
        trackName Text,
        artistName Text,
        albumName Text,
        trackUri Text
        )
    ''')
    connection.commit()
    for item in items:
        item = item['track']
        trackName = item['trackName']
        artistName = item['artistName']
        albumName = item['albumName']
        trackUri = item['trackUri']
        cursor.execute(f"INSERT INTO {name} (trackName, artistName, albumName, trackUri) VALUES (?, ?, ?, ?)", (trackName, artistName, albumName, trackUri, ))
        connection.commit()
    connection.commit()
