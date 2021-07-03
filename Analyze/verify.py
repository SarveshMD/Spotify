import json
import sqlite3

playlists = json.loads(open("../MySpotifyData/Playlist1.json").read())['playlists']
history = json.loads(open("../MySpotifyData/StreamingHistory0.json").read())

# print(f"Length of playlists : {len(playlists)}\n\n")
# for playlist in playlists:
#     print(f"Playlist name: {playlist['name']}")
#     items = playlist['items']
#     print(f"Length of items: {len(items)}")
#     print()
allSongs = list()

for song in history:
    songName = song['trackName']
    if not songName in allSongs:
        allSongs.append(songName)

for playlist in playlists:
    for song in playlist['items']:
        songName = song['track']['trackName']
        if not songName in allSongs:
            allSongs.append(songName)
        else:
            print(songName)

print(len(allSongs))
connection = sqlite3.connect("../Databases/songsArtists.sqlite")
cursor = connection.cursor()

cursor.execute("SELECT * FROM Songs")
songs = cursor.fetchall()
for song in songs:
    trackName = song[1]
    if not trackName in allSongs:
        print(song)