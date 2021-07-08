import sqlite3
import datetime
from tabulate import tabulate

connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()
songsArtistConnection = sqlite3.connect("../Databases/songsArtists.sqlite")
songsArtistCursor = songsArtistConnection.cursor()
cursor.execute("SELECT * FROM streamingHistory ORDER BY endTime ASC")
streamingHistory = cursor.fetchall()

summary = {}
for song in streamingHistory:
    endTime = song[0]
    fullDate = endTime.split()[0].split("-")
    fullTime = endTime.split()[1].split(":")
    year = int(fullDate[0])
    month = int(fullDate[1])
    date = int(fullDate[2])
    hour = int(fullTime[0])
    second = int(fullTime[1])
    # endTime = str(datetime.datetime(year, month, date, hour, second))
    endTime = datetime.datetime(year, month, date, hour, second)
    trackId = song[1]
    if not trackId in summary.keys():
        summary[trackId] = [endTime]
    else:
        summary[trackId].append(endTime)

cursor.execute("SELECT trackId FROM streamingHistory")
analyzeTrackIdSDupe = cursor.fetchall()
analyzeTrackIds = list()
for trackId in analyzeTrackIdSDupe:
    analyzeTrackIds.append(trackId[0])
songResults = {}
for analyzeTrackId in analyzeTrackIds:
    songResult = {}
    for item in summary[analyzeTrackId]:
        if str(item.hour) not in songResult.keys():
            songResult[str(item.hour)] = 1
        else:
            songResult[str(item.hour)] += 1
    songResults[analyzeTrackId] = songResult

table = list()

for trackId, trackHistory in songResults.items():
    maxTimesForThisSong = None
    maxHourForThisSong = None
    for hour, times in trackHistory.items():
        if maxTimesForThisSong is None or maxTimesForThisSong <= times:
            maxTimesForThisSong = times
            maxHourForThisSong = hour
    maxHourForThisSong = int(maxHourForThisSong)
    if maxHourForThisSong > 12:
        maxHourForThisSong = str(maxHourForThisSong % 12) + " PM"
    elif maxHourForThisSong == 12:
        maxHourForThisSong = str(maxHourForThisSong) + " PM"
    else:
        maxHourForThisSong = str(maxHourForThisSong) + " AM"
    songsArtistCursor.execute("SELECT trackName FROM songs WHERE id IS ?", (trackId,))
    trackName = songsArtistCursor.fetchone()[0]
    table.append([trackName, maxHourForThisSong,maxTimesForThisSong])

table = tabulate(table, headers=['Song Name', "Most Frequently Played", "No. Of Times"], tablefmt="pipe", colalign=("left", "center","right"))
print()
print(table)

# TODO
# Get the results based on time of listening
#   - When a particular song is listened to most frequently
