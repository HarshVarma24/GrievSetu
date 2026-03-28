from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    
    @field_validator("confirm_password")
    def passwords_match(cls, confirm_password, info):
        if "password" in info.data and confirm_password != info.data["password"]:
            raise ValueError("Passwords do not match")
        return confirm_password

class UserLogin(BaseModel):
    name: str
    password: str

class GrievanceRequest(BaseModel):
    text: str
    
