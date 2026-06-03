from auth.dtos.dtos import ChangePasswordDTO
from auth.services.passwordValidator import validate_password
from auth.services.passwordHasher import hash_password, verify_password
from database.connection import connection, cursor
from auth.services.passwordHistory import password_in_history,save_password_history


def change_password_service(user: ChangePasswordDTO):
    errors = validate_password(user.new_password)
    if errors:
        return {"message": errors[0]}

    if password_in_history(user.username,user.new_password):
        return{"message":"You can use youre recent passwords"}
    

    try:
        cursor.execute(
            """
            SELECT username, password, salt FROM users WHERE username = ?
            """,
            (user.username,)
        )
        existing_user = cursor.fetchone()

        if existing_user is None:
            raise Exception("Username does not exist")

        if not verify_password(user.current_password, existing_user[1], existing_user[2]):
            raise Exception("Current password is incorrect")

    except Exception as e:
        return {"message": str(e)}

    new_hash, new_salt = hash_password(user.new_password)

    try:
        cursor.execute(
            """
            UPDATE users
            SET password = ?, salt = ?
            WHERE username = ?
            """,
            (new_hash, new_salt, user.username)
        )
        connection.commit()

        save_password_history(user.username,new_hash,new_salt)
        
        return {"message": "Password changed successfully"}

    except Exception as e:
        return {
            "message": "Change password failed",
            "error": str(e)
        }
