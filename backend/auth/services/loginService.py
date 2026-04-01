import sqlite3
from auth.dtos.dtos import LoginDTO
from database.connection import connection, cursor

def login_service(user: LoginDTO):

    try:
        cursor.execute(
            f"""
            select username FROM users WHERE username = '{user.username}' AND password = '{user.password}'
            """
        )

        existing_user = cursor.fetchone()
        
        if existing_user:
            return {
                "message": "Login successful",
                "username": existing_user[0]
            }
        
        else:
            return {
                "message": "Invalid username or password"
            }


    except Exception as e:
        return {
            "message": "Login Failed",
            "error": str(e)
        }