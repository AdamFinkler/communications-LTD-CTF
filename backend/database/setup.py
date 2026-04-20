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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    package_name TEXT NOT NULL UNIQUE,
    download_speed INTEGER NOT NULL,
    upload_speed INTEGER NOT NULL,
    monthly_price REAL NOT NULL
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    package_id INTEGER NOT NULL, 
    FOREIGN KEY (package_id) REFERENCES packages(id)
)
""")


connection.commit()