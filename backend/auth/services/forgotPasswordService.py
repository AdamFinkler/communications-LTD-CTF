from auth.dtos.dtos import ForgotPasswordDTO
from auth.utils.password_utils import create_reset_token, verify_reset_token
from database.connection import cursor


def _send_reset_email(to_email: str, token: str) -> None:
    print(f"[Forgot Password] One-time reset code for {to_email}: {token}")


def forgot_password_service(user: ForgotPasswordDTO):
    if user.code:
        if verify_reset_token(user.email, user.code):
            return {"message": "Password reset successful", "verified": True}
        return {"message": "Invalid verification code"}

    try:
        cursor.execute(
            f"""
            SELECT email FROM users WHERE email = '{user.email}'
            """
        )
        existing_user = cursor.fetchone()

        if not existing_user:
            return {"message": "Email does not exist"}

        token = create_reset_token(user.email)
        _send_reset_email(existing_user[0], token)

        return {
            "message": "Password reset code sent to email",
            "hint": "Check the backend console for the demo reset code",
        }

    except Exception as e:
        return {
            "message": "Password reset failed",
            "error": str(e),
        }
