from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# --------- Schemas de entrada ----------
class LoginIn(BaseModel):
    email: EmailStr
    password: str


# --------- Helper ----------
def _get_current_user(db: Session, authorization: str | None) -> User:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Token ausente")
    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)
    uid = payload.get("sub")
    if not uid:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.get(User, uid)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user


# --------- Endpoints ----------
@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")

    obj = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(payload.password),  # já corta em 72 bytes na função
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.post("/login")
def login(info: LoginIn, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == info.email)).scalar_one_or_none()
    if not user or not verify_password(info.password, user.password_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos")

    token = create_access_token({"sub": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
        },
    }


@router.get("/me", response_model=UserOut)
def me(Authorization: str | None = Header(None), db: Session = Depends(get_db)):
    user = _get_current_user(db, Authorization)
    return user
