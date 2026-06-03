from auth.dtos.dtos import ChangePasswordAVDTO
from auth.utils.password_utils import (
    check_password_history,
    clear_reset_verification,
    hash_password,
    is_reset_verified,
    save_password_history,
    validate_password,
)
from database.connection import connection, cursor


def change_password_after_verification_service(user: ChangePasswordAVDTO):
    if not is_reset_verified(user.email):
        return {"message": "Complete forgot-password verification before changing password"}

    try:
        cursor.execute(
            f"""
            SELECT username, salt FROM users WHERE email = '{user.email}'
            """
        )
        existing_user = cursor.fetchone()

        if existing_user is None:
            return {"message": "User does not exist"}

        username, salt = existing_user

        is_valid, error_message = validate_password(user.new_password, username)
        if not is_valid:
            return {"message": error_message}

        history_ok, history_message = check_password_history(
            username, user.new_password, salt
        )
        if not history_ok:
            return {"message": history_message}

        new_hash = hash_password(user.new_password, salt)

        cursor.execute(
            f"""
            UPDATE users
            SET password = '{new_hash}'
            WHERE email = '{user.email}'
            """
        )
        save_password_history(username, new_hash)
        connection.commit()
        clear_reset_verification(user.email)

        return {"message": "Password changed successfully"}

    except Exception as e:
        return {
            "message": "Change password failed",
            "error": str(e),
        }
