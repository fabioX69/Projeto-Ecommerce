# app/schemas/user.py
from pydantic import BaseModel, EmailStr, constr

# Base: campos comuns do usuário
class UserBase(BaseModel):
    full_name: constr(strip_whitespace=True, min_length=1)
    email: EmailStr

# Para criação de usuário (registro)
class UserCreate(UserBase):
    password: constr(min_length=6, max_length=128)

# Para retorno (saída)
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr

    class Config:
        from_attributes = True  # pydantic v2 (antes chamava orm_mode = True)

# Para login (sem full_name)
class LoginInput(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=128)


