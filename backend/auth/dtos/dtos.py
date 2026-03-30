from pydantic import BaseModel, EmailStr

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
    username: Optional[str] = None
    email: Optional[EmailStr] = None