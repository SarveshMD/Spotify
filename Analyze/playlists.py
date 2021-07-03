import json
import sqlite3

connection = sqlite3.connect("../Databases/playlists.sqlite")
cursor = connection.cursor()
playlists = json.loads(open("../MySpotifyData/Playlist1.json").read())['playlists']
songsArtistsConnection = sqlite3.connect("../Databases/songsArtists.sqlite")
songsArtistsCursor = songsArtistsConnection.cursor()

for playlist in playlists:
    name = playlist['name'].replace(" ", "_")
    items = playlist['items']
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {name}
        (
        trackId Text,
        artistId Text,
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
        songsArtistsCursor.execute("SELECT id from Artists WHERE artistName IS ( ? )", (artistName, ) )
        artistId = songsArtistsCursor.fetchone()[0]
        songsArtistsCursor.execute("SELECT id from Songs WHERE trackName IS ( ? )", (trackName, ) )
        trackId = songsArtistsCursor.fetchone()[0]
        print((trackId, artistId, albumName, trackUri))
        cursor.execute(f"INSERT INTO {name} (trackId, artistId, albumName, trackUri) VALUES (?, ?, ?, ?)", (trackId, artistId, albumName, trackUri, ))
        connection.commit()
    connection.commit()
