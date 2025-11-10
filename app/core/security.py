# app/core/security.py
from datetime import datetime, timedelta
from typing import Any, Dict

from jose import jwt, JWTError
from passlib.context import CryptContext

# ⚠️ trocamos de bcrypt -> pbkdf2_sha256 para evitar erro de backend
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT
SECRET_KEY = "CHANGE-ME-TO-A-VERY-LONG-SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False
    return pwd_context.verify(plain, hashed)

def create_access_token(data: Dict[str, Any], expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> Dict[str, Any] | None:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
