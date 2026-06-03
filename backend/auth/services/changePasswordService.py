from auth.dtos.dtos import ChangePasswordDTO
from auth.utils.password_utils import (
    check_password_history,
    generate_salt,
    hash_password,
    save_password_history,
    validate_password,
    verify_password,
)
from database.connection import connection, cursor


def change_password_service(user: ChangePasswordDTO):
    try:
        cursor.execute(
            f"""
            SELECT username, password, salt FROM users WHERE username = '{user.username}'
            """
        )
        existing_user = cursor.fetchone()

        if existing_user is None:
            return {"message": "Username does not exist"}

        _, stored_hash, salt = existing_user

        if not verify_password(user.current_password, salt, stored_hash):
            return {"message": "Current password is incorrect"}

        is_valid, error_message = validate_password(user.new_password, user.username)
        if not is_valid:
            return {"message": error_message}

        history_ok, history_message = check_password_history(
            user.username, user.new_password, salt
        )
        if not history_ok:
            return {"message": history_message}

        new_hash = hash_password(user.new_password, salt)

        cursor.execute(
            f"""
            UPDATE users
            SET password = '{new_hash}'
            WHERE username = '{user.username}'
            """
        )
        save_password_history(user.username, new_hash)
        connection.commit()

        return {"message": "Password changed successfully"}

    except Exception as e:
        return {
            "message": "Change password failed",
            "error": str(e),
        }
