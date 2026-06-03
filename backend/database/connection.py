import sqlite3

connection = sqlite3.connect("database/database.db", check_same_thread=False)

cursor = connection.cursor()

import database.setup  # noqa: E402, F401