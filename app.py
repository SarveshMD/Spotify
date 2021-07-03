import json
import sqlite3
import sys

# Reset sqlite file
try :
    if sys.argv[1].lower() == "reset":
        connection = sqlite3.connect("spotify.sqlite")
        cursor = connection.cursor()
        cursor.execute("DROP TABLE  IF EXISTS StreamingHistory")
        cursor.execute("CREATE TABLE IF NOT EXISTS StreamingHistory (endTime, artistName, trackName, msPlayed)")
except IndexError :
    pass

streamingHistory = json.loads(open("MySpotifyData/StreamingHistory0.json").read())
