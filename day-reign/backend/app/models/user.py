from pydantic import BaseModel, EmailStr, Field

class RegisterInput(BaseModel):
    name: str = Field(min_length=1, max_length=800)
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr