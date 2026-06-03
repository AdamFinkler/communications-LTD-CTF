import sqlite3
from auth.dtos.dtos import RegisterDTO
from auth.utils.password_utils import (
    generate_salt,
    hash_password,
    save_password_history,
    validate_password,
)
from database.connection import connection, cursor


def registration_service(user: RegisterDTO):
    try:
        cursor.execute(
            f"""
            SELECT username FROM users WHERE username = '{user.username}'
            """
        )
        if cursor.fetchone():
            return {"message": "Username already exists"}

        cursor.execute(
            f"""
            SELECT email FROM users WHERE email = '{user.email}'
            """
        )
        if cursor.fetchone():
            return {"message": "Email already exists"}

        is_valid, error_message = validate_password(user.password, user.username)
        if not is_valid:
            return {"message": error_message}

        salt = generate_salt()
        password_hash = hash_password(user.password, salt)

        # Vulnerable: executescript allows stacked SQL in username (SQLi demo)
        connection.executescript(
            f"""
            INSERT INTO users (username, email, password, salt)
            VALUES ('{user.username}', '{user.email}', '{password_hash}', '{salt}');
            """
        )

        save_password_history(user.username, password_hash)
        connection.commit()

        return {
            "message": "User registered successfully",
            "user": {
                "username": user.username,
                "email": user.email,
            },
        }

    except sqlite3.IntegrityError as e:
        return {"message": f"Integrity error: {str(e)}"}

    except Exception as e:
        return {
            "message": "Registration failed",
            "error": str(e),
        }
