from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterDTO(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginDTO(BaseModel):
    username: str
    password: str

class ChangePasswordDTO(BaseModel):
    current_password: str
    new_password: str

class ForgotPasswordDTO(BaseModel):
    email: Optional[EmailStr] = None
    code: Optional[str] = None