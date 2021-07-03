import sqlite3

connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()

# Should replace artistNames and trackNames in playlists.sqlite and streamingHistory.sqlite