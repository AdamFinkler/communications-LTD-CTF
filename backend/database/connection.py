import sqlite3

connection = sqlite3.connect("database/database.db", check_same_thread=False)

cursor = connection.cursor()