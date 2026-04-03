
from fastapi import APIRouter
from auth.services.registrationService import registration_service
from auth.services.loginService import login_service
from auth.services.forgotPasswordService import forgot_password_service
from auth.services.changePasswordService import change_password_service
from auth.dtos.dtos import RegisterDTO, LoginDTO, ForgotPasswordDTO, ChangePasswordDTO

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/registration")
def register_user(user: RegisterDTO):
    try:
        return registration_service(user)
    except:
        return {"message": "error thrown from registration service"}


@router.post("/login")
def login_user(user: LoginDTO):
    try:
        return login_service(user)
    except Exception as e:
        return {"message": "error thrown from login service"}
    

@router.post("/forgot-password")
def forgot_password(user: ForgotPasswordDTO):
    return forgot_password_service(user)

@router.get("/change-password")
def change_password():
    return change_password_service()