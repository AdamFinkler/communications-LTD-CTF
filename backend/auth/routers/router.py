
from fastapi import APIRouter
from auth.services.registrationService import registration_service
from auth.services.loginService import login_service
from auth.services.forgotPasswordService import forgot_password_service
from auth.services.changePasswordService import change_password_service
from auth.services.changePasswordAfterVerificationService import change_password_after_verification_service
from auth.dtos.dtos import (
    RegisterDTO,
    LoginDTO,
    ForgotPasswordDTO,
    ChangePasswordDTO,
    CreateCustomerDTO,
    ChangePasswordAVDTO,
    DeleteCustomerDTO,
)
from auth.services.deleteCustomerService import delete_customer_service
from auth.services.createCustomerService import create_customer_service
from auth.services.deleteAllCustomersService import delete_all_customers_service
from auth.services.listCustomersService import list_customers_service
from auth.utils.password_utils import load_password_config

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/password-config")
def get_password_config():
    return load_password_config()


@router.post("/registration")
def register_user(user: RegisterDTO):
    try:
        return registration_service(user)
    except Exception:
        return {"message": "error thrown from registration service"}


@router.post("/login")
def login_user(user: LoginDTO):
    try:
        return login_service(user)
    except Exception:
        return {"message": "error thrown from login service"}


@router.post("/forgot-password")
def forgot_password(user: ForgotPasswordDTO):
    return forgot_password_service(user)


@router.post("/change-password")
def change_password_post(user: ChangePasswordDTO):
    try:
        return change_password_service(user)
    except Exception:
        return {"message": "error thrown from change password service"}


@router.post("/change-password-after-verification")
def change_password_after_verification(user: ChangePasswordAVDTO):
    try:
        return change_password_after_verification_service(user)
    except Exception:
        return {"message": "error thrown from change password after verification service"}


@router.get("/customers")
def list_customers():
    return list_customers_service()


@router.delete("/delete-customer/{customer_id}")
def delete_customer(customer_id: int):
    return delete_customer_service(customer_id)


@router.post("/delete-customer")
def delete_customer_post(body: DeleteCustomerDTO):
    return delete_customer_service(body.customer_id)


@router.delete("/delete-all-customers")
def delete_all_customers():
    return delete_all_customers_service()


@router.post("/create-customer")
def create_customer(customer: CreateCustomerDTO):
    return create_customer_service(customer.package_id, customer.customer_name)
