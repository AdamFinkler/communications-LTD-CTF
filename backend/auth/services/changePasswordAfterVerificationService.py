from auth.dtos.dtos import ChangePasswordAVDTO
from auth.services.passwordValidator import validate_password
from database.connection import connection, cursor


def change_password_service_after_verification_service(user: ChangePasswordAVDTO):
    errors = validate_password(user.new_password)
    if errors:
        return {"message": errors[0]}

    try:
        cursor.execute(
            """
            UPDATE users
            SET password = ?
            WHERE username = ?
            """,
            (user.new_password, user.username)
        )
        connection.commit()

        return {"message": "Password changed successfully"}

    except Exception as e:
        return {
            "message": "Change password failed",
            "error": str(e)
        }
