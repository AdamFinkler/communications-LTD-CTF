from auth.dtos.dtos import ChangePasswordDTO
from auth.services.passwordValidator import validate_password
from database.connection import connection, cursor


def change_password_service(user: ChangePasswordDTO):
    errors = validate_password(user.new_password)
    if errors:
        return {"message": errors[0]}

    try:
        cursor.execute(
            """
            SELECT username, password FROM users WHERE username = ?
            """,
            (user.username,)
        )
        existing_user = cursor.fetchone()

        if existing_user is None:
            raise Exception("Username does not exist")

        if existing_user[1] != user.current_password:
            raise Exception("Current password is incorrect")

    except Exception as e:
        return {"message": str(e)}

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
