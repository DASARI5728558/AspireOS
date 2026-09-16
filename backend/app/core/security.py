from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status
from .config import get_settings

pwd = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(value: str) -> str:
    return pwd.hash(value)


def verify_password(raw: str, hashed: str) -> bool:
    return pwd.verify(raw, hashed)


def create_token(subject: str, role: str) -> str:
    s = get_settings()
    payload = {"sub": subject, "role": role, "exp": datetime.now(timezone.utc) + timedelta(minutes=s.access_token_minutes)}
    return jwt.encode(payload, s.secret_key, algorithm="HS256")


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, get_settings().secret_key, algorithms=["HS256"])
    except JWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc
