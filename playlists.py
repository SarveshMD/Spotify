import json
import sqlite3

connection = sqlite3.connect("playlists.sqlite")
cursor = connection.cursor()
playlists = json.loads(open("MySpotifyData/Playlist1.json").read())['playlists']

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

# Sample data from Playlist1.json
# {
#   "playlists": [
#     {
#       "name": "Energy",
#       "lastModifiedDate": "2021-06-07",
#       "items": [
#         {
#           "track": {
#             "trackName": "Thangamey",
#             "artistName": "Anirudh Ravichander",
#             "albumName": "Naanum Rowdy Dhaan (Original Motion Picture Soundtrack)",
#             "trackUri": "spotify:track:62KDpF0Hv7KJLZrrKXsz8r"
#           },
#           "episode": null,
#           "localTrack": null
#         },
#         {
#           "track": {
#             "trackName": "En Iniya Thanimaye",
#             "artistName": "D. Imman",
#             "albumName": "Teddy",
#             "trackUri": "spotify:track:5z7IJoDX9iOavWOS1Y8zOy"
#           },
#           "episode": null,
#           "localTrack": null
#         }
#       ],
#       "description": null,
#       "numberOfFollowers": 0
#     }
#   ]
# }