from fastapi import HTTPException, status
import sqlite3
from auth.dtos.dtos import RegisterDTO
from auth.services.passwordValidator import validate_password
from auth.services.passwordHasher import hash_password
from database.connection import connection, cursor

def registration_service(user: RegisterDTO):
    errors = validate_password(user.password)
    if errors:
        return {"message": errors[0]}

    password_hash, salt = hash_password(user.password)

    try:
        cursor.execute(
            """
            INSERT INTO users (username, email, password, salt)
            VALUES (?, ?, ?, ?)
            """,
            (user.username, user.email, password_hash, salt)
        )

        connection.commit()

        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "User registered successfully",
            "user": {
                "username": user.username,
                "email": user.email
            }
        }

    except sqlite3.IntegrityError as e:
        return {"message": f"Integrity error: {str(e)}"}

    except Exception as e:
        return {
            "message": "Registration failed",
            "error": str(e)
        }
