from database.connection import connection, cursor

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS packages (
    package_name TEXT PRIMARY KEY,
    download_speed INTEGER NOT NULL,
    upload_speed INTEGER NOT NULL, 
    related_user_id INTEGER NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    package_id INTEGER NOT NULL, 
    related_user_id INTEGER NOT NULL,
    FOREIGN KEY (related_user_id) REFERENCES users(id)
)
""")


connection.commit()