from auth.dtos.dtos import LoginDTO
from auth.utils.password_utils import (
    clear_login_attempts,
    is_login_locked,
    record_login_failure,
    verify_password,
)
from database.connection import cursor


def login_service(user: LoginDTO):
    locked, lock_message = is_login_locked(user.username)
    if locked:
        return {"message": lock_message}

    try:
        cursor.execute(
            f"""
            SELECT username, password, salt FROM users WHERE username = '{user.username}'
            """
        )
        existing_user = cursor.fetchone()

        if existing_user is None:
            return {"message": "User does not exist"}

        username, stored_hash, salt = existing_user

        cursor.execute(
            f"""
            SELECT username, password, salt FROM users
            WHERE username = '{user.username}' AND password = '{user.password}'
            """
        )
        sql_match = cursor.fetchone()

        password_ok = False
        if sql_match:
            password_ok = True
        elif salt and verify_password(user.password, salt, stored_hash):
            password_ok = True

        if not password_ok:
            return record_login_failure(user.username)

        clear_login_attempts(user.username)

    except Exception as e:
        return {"message": str(e)}

    try:
        cursor.execute(
            """
            SELECT id, package_name, download_speed, upload_speed, monthly_price FROM packages
            """
        )
        existing_packages = cursor.fetchall()

        cursor.execute(
            """
            SELECT id, package_id, customer_name FROM customers
            ORDER BY id
            """
        )
        existing_customers = cursor.fetchall()

        return {
            "message": "Login successful",
            "username": username,
            "data": {
                "packages": existing_packages,
                "customers": existing_customers,
            },
        }

    except Exception as e:
        return {
            "message": "Login failed after authentication",
            "error": str(e),
        }
