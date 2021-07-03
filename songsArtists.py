import json
import sqlite3

streamingHistory = json.loads(open("MySpotifyData/StreamingHistory0.json").read())
playlists = json.loads(open("MySpotifyData/Playlist1.json").read())['playlists']

connection = sqlite3.connect("songsArtists.sqlite")
cursor = connection.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS Songs
(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    trackName Text UNIQUE,
    artistId INTEGER,
    albumName Text,
    trackUri Text UNIQUE
);
CREATE TABLE IF NOT EXISTS Artists
(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    artistName Text UNIQUE,
    NOSongsInPlaylist Integer
)
''')
connection.commit()

playlistSongs = list()
allSongs = list()
artists = list()
artistWrittenToFile = list()
artistPoint = {}

for playlist in playlists:
    items = playlist['items']
    for item in items:
        item = item['track']
        trackName = item['trackName']
        artistName = item['artistName']
        if not (trackName in playlistSongs):
            allSongs.append(item)
            playlistSongs.append(trackName)
        if not (artistName in artists):
            artists.append(artistName)

artistPointCreated = list()
for song in allSongs:
    artistName = song['artistName']
    if artistName not in artistPointCreated:
        artistPoint[artistName] = 0
        artistPointCreated.append(artistName)
    artistPoint[artistName] += 1

for song in allSongs:
    trackName = song['trackName']
    artistName = song['artistName']
    albumName = song['albumName']
    trackUri = song['trackUri']
    if artistName not in artistWrittenToFile:
        cursor.execute('''
        INSERT INTO Artists ( artistName, NOSongsInPlaylist ) VALUES ( ?, ? )
        ''', ( artistName, artistPoint[artistName] ) )
        artistWrittenToFile.append(artistName)
    cursor.execute("SELECT id from Artists WHERE artistName IS ( ? )", (artistName, ) )
    artistId = cursor.fetchone()[0]
    cursor.execute('''
    INSERT INTO Songs
    (trackName, artistId, albumName, trackUri) VALUES ( ?, ?, ?, ? )
    ''', (trackName, artistId , albumName, trackUri))
    connection.commit()
