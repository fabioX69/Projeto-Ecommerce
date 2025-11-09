from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import verify_password, hash_password, create_access_token, decode_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    obj = User(full_name=payload.full_name, email=payload.email, password_hash=hash_password(payload.password))
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.email == form_data.username)).scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")
    token = create_access_token(str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def me(token: str, db: Session = Depends(get_db)):
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.get(User, int(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
