from auth.dtos.dtos import ChangePasswordAVDTO
from auth.services.passwordValidator import validate_password
from auth.services.passwordHasher import hash_password
from database.connection import connection, cursor
from auth.services.passwordHistory import password_in_history,save_password_history

def change_password_service_after_verification_service(user: ChangePasswordAVDTO):
    errors = validate_password(user.new_password) 
    if errors:
        return {"message": errors[0]}

    if password_in_history(user.username,user.new_password):
        return{"message":"You can't use your recent passwords"}
    
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
        
        connection.commit()
        return {"message": "Password changed successfully"}

    except Exception as e:
        return {
            "message": "Change password failed",
            "error": str(e)
        }
