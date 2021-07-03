import json
playlists = json.loads(open("../MySpotifyData/Playlist1.json").read())['playlists']

print(f"Length of playlists : {len(playlists)}\n\n")
for playlist in playlists:
    print(f"Playlist name: {playlist['name']}")
    items = playlist['items']
    print(f"Length of items: {len(items)}")
    print()