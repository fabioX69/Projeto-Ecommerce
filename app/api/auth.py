from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic import BaseModel, EmailStr

from app.db.session import get_db
from app.models.user import User
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    """
    Aceita tanto JSON {"email": "...", "password": "..."} quanto form-urlencoded.
    """
    try:
        content_type = (request.headers.get("content-type") or "").lower()
        if "application/json" in content_type:
            data = await request.json()
        else:
            form = await request.form()
            data = dict(form)

        email = (data.get("email") or data.get("username") or "").strip()
        password = data.get("password") or ""

    except Exception:
        raise HTTPException(status_code=400, detail="Erro ao ler corpo da requisição")

    # Validação manual e com Pydantic
    if not email or not password:
        raise HTTPException(status_code=422, detail="Campos obrigatórios: email e senha")

    try:
        # Instancia o modelo LoginIn (valida o formato do e-mail automaticamente)
        login_data = LoginIn(email=email, password=password)
    except Exception as e:
        raise HTTPException(status_code=422, detail="E-mail inválido")

    # Busca o usuário no banco
    user = db.execute(select(User).where(User.email == login_data.email)).scalar_one_or_none()
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas")

    # Cria token JWT
    token = create_access_token({"sub": str(user.id), "email": user.email})

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "full_name": user.full_name, "email": user.email},
    }
