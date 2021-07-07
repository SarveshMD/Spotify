import sqlite3
connection = sqlite3.connect("../Databases/streamingHistory.sqlite")
cursor = connection.cursor()

# TODO
# Get the results based on time of listening
#   - When a particular song is listened to most frequently