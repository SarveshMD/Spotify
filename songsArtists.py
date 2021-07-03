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
    name Text,
    artistId INTEGER,
    album Text,
    uri Text
);
CREATE TABLE IF NOT EXISTS Artists
(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name Text
)
''')

historySongs = list()
playlistSongs = list()
notInPlaylist = list()
notInHistory = list()

for song in streamingHistory:
    # endTime = song['endTime']
    # artistName = song['artistName']
    trackName = song['trackName']
    # msPlayed = song['msPlayed']
    if not (trackName in historySongs):
        historySongs.append(trackName)

for playlist in playlists:
    # name = playlist['name'].replace(" ", "_")
    items = playlist['items']
    for item in items:
        item = item['track']
        trackName = item['trackName']
        # artistName = item['artistName']
        # albumName = item['albumName']
        # trackUri = item['trackUri']
        if not (trackName in playlistSongs):
            playlistSongs.append(trackName)

# print("Playlist songs: \n", playlistSongs)
# print("\n\n")
# print("History songs: \n", historySongs)

for song in historySongs:
    if song not in playlistSongs:
        for playlistSong in playlistSongs:
            if song[:10] in playlistSong:
                print(f"{playlistSong}\n{song}\n")

# for song in playlistSongs:
#     if song not in historySongs:
#         notInHistory.append(song)
#         print(song)
