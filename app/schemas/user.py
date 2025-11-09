from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    class Config:
        from_attributes = True
