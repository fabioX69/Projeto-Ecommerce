from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _prep(p: str) -> str:
    if not p:
        return ""
    # remove espaços “fantasma” de começo/fim e garante <=72 bytes
    p = p.strip()
    p = p.encode("utf-8")[:72].decode("utf-8", errors="ignore")
    return p

def hash_password(plain: str) -> str:
    plain = _prep(plain)
    return pwd_context.hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    plain = _prep(plain)
    return pwd_context.verify(plain, hashed)

SECRET_KEY = getattr(settings, "SECRET_KEY", "changeme123")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = getattr(settings, "ACCESS_TOKEN_EXPIRE_MINUTES", 60)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None

