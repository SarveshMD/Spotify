import sqlite3
from datetime import timedelta
from tabulate import tabulate

connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()
songsArtistsConn = sqlite3.connect("../Databases/songsArtists.sqlite")
songsArtistsCursor = songsArtistsConn.cursor()

cursor.execute("SELECT * FROM artistSummary ORDER BY totalMsPlayed DESC")
summaryFromTable = cursor.fetchall()

i = 0
table = list()
for artistId, totalMsPlayed in summaryFromTable:
    i += 1
    songsArtistsCursor.execute(f'SELECT artistName FROM Artists WHERE id IS {artistId}')
    artistName = songsArtistsCursor.fetchone()[0]
    convertedPlayed = str(timedelta(milliseconds=totalMsPlayed)).split(":")
    hours = int(convertedPlayed[0])
    minutes = int(convertedPlayed[1])
    seconds = float(convertedPlayed[2])
    table.append([i, artistName, hours, minutes, f"{seconds:.2f}"])
table = tabulate(table, headers=['S.No', 'Artist Name', 'Hours', 'Minutes', 'Seconds'], tablefmt="pipe")
print()
print(table)
