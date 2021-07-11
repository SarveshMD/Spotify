import json
import sqlite3

streamingHistory = json.loads(open("../MySpotifyData/StreamingHistory0.json").read())
playlists = json.loads(open("../MySpotifyData/Playlist1.json").read())['playlists']

connection = sqlite3.connect("../Databases/songsArtists.sqlite")
cursor = connection.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS Songs
(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    trackName TEXT UNIQUE,
    artistId INTEGER,
    albumId INTEGER,
    trackUri TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS Artists
(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    artistName TEXT UNIQUE
);
CREATE TABLE IF NOT EXISTS Albums
(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    albumName TEXT Unique
)
''')
connection.commit()

playlistSongs = list()
historySongs = list()
allSongs = list()
artists = list()
artistWrittenToFile = list()
albums = list()
albumWrittenToFile = list()

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

for song in streamingHistory:
    trackName = song['trackName']
    artistName = song['artistName']
    if not (trackName in historySongs) and not (trackName in playlistSongs):
        historySongs.append(trackName)
        allSongs.append({'trackName': trackName, 'artistName': artistName, 'albumName': None, 'trackUri': None})

for song in allSongs:
    trackName = song['trackName']
    artistName = song['artistName']
    albumName = song['albumName']
    trackUri = song['trackUri']
    cursor.execute('''
    INSERT OR IGNORE INTO Artists ( artistName ) VALUES ( ? )
    ''', ( artistName, ) )
    cursor.execute('''
    INSERT OR IGNORE INTO Albums ( albumName ) VALUES ( ? )
    ''', ( albumName, ))
    cursor.execute("SELECT id from Artists WHERE artistName IS ( ? )", (artistName, ) )
    artistId = cursor.fetchone()[0]
    cursor.execute("SELECT id from Albums WHERE albumName IS ( ? )", (albumName, ) )
    albumId = cursor.fetchone()[0]
    cursor.execute('''
    INSERT OR IGNORE INTO Songs
    (trackName, artistId, albumId, trackUri) VALUES ( ?, ?, ?, ? )
    ''', (trackName, artistId , albumId, trackUri))
    print(trackName, artistId , albumId, trackUri)
connection.commit()
