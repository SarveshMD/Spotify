import sqlite3
from datetime import timedelta
from tabulate import tabulate
# import json

connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()
songsArtistsConn = sqlite3.connect("../Databases/songsArtists.sqlite")
songsArtistsCursor = songsArtistsConn.cursor()

summary = {}
cursor.execute('''
CREATE TABLE IF NOT EXISTS summary (
    trackId INTEGER UNIQUE,
    totalMsPlayed INTEGER
    )
''')
cursor.execute('SELECT * FROM streamingHistory')
streamingHistory = cursor.fetchall()
for item in streamingHistory:
    endTime = item[0]
    trackId = item[1]
    artistId = item[2]
    msPlayed = item[3]
    if trackId not in summary.keys():
        summary[trackId] =  msPlayed
    else :
        summary[trackId] += msPlayed

# print(json.dumps({int(key):summary[key] for key in summary.keys()}, indent=4, sort_keys=True))

for trackId, totalMsPlayed in summary.items():
    cursor.execute("INSERT OR IGNORE INTO summary (trackId, totalMsPlayed) VALUES (?, ?)", (trackId, totalMsPlayed))
connection.commit()

cursor.execute("SELECT * FROM summary ORDER BY totalMsPlayed DESC")
summaryFromTable = cursor.fetchall()



i = 0
table = list()
for trackId, totalMsPlayed in summaryFromTable:
    i += 1
    songsArtistsCursor.execute(f'''SELECT trackName FROM Songs WHERE id IS {trackId}''')
    trackName = songsArtistsCursor.fetchone()[0]
    convertedPlayed = str(timedelta(milliseconds=totalMsPlayed)).split(":")
    hours = int(convertedPlayed[0])
    minutes = int(convertedPlayed[1])
    seconds = float(convertedPlayed[2])
    table.append([i, trackName, hours, minutes, f"{seconds:.2f}"])
table = tabulate(table, headers=['S.No', 'Track Name', 'Hours', 'Minutes', 'Seconds'], tablefmt="pipe")
print()
print(table)
# maxMsPlayed = None
# minMsPlayed = None
# maxPlayedTrackId = int()
# minPlayedTrackId = int()

# for trackId,msPlayed in summary.items() :
#     if minMsPlayed is None or msPlayed <= minMsPlayed:
#         minMsPlayed = msPlayed
#         minPlayedTrackId = trackId
#     elif maxMsPlayed is None or msPlayed >= maxMsPlayed:
#         maxMsPlayed = msPlayed
#         maxPlayedTrackId = trackId

# songsArtistsCursor.execute(f'''
# SELECT trackName FROM Songs WHERE id IS {maxPlayedTrackId}
# ''')
# maxPlayedTrackName = songsArtistsCursor.fetchone()[0]

# songsArtistsCursor.execute(f'''
# SELECT trackName FROM Songs WHERE id IS {minPlayedTrackId}
# ''')
# minPlayedTrackName = songsArtistsCursor.fetchone()[0]

# print(f"Most Favorite Song: {maxPlayedTrackName}\nSeconds Played: {maxMsPlayed}\n")
# print(f"Least Favorite Song: {minPlayedTrackName}\nSeconds Played: {minMsPlayed}\n")

# Get the results based on length of listening
#    Most favorite Song
#    Most favorite Artist

# Sample Data :
# [
# ('2020-11-21 05:24', '43', '2', 285190),
# ('2020-11-21 05:24', '43', '2', 285190)
# ]
