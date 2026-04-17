import sqlite3
from auth.dtos.dtos import LoginDTO
from database.connection import connection, cursor

def login_service(user: LoginDTO):



    try:
        cursor.execute(
            f"""
            select username FROM users WHERE username = '{user.username}'
            """
        )
        

        existing_user = cursor.fetchone()

        if existing_user == None:
            raise Exception("Username does not exist")
        
    except Exception as e:
        return{
            "message": str(e)
        }



    try:
        cursor.execute(
            f"""
            select username, password FROM users WHERE username = '{user.username}' AND password = '{user.password}'
            """
        )

        existing_user = cursor.fetchone()
        
        if existing_user == None:

            raise Exception("Wrong password")


        return {
                "message": "Login successful",
                "username": existing_user[0]
            }
        


    except Exception as e:
        return {
            "message": "Login Failed",
            "error": str(e)
        }