"""
Hand-rolled JWT auth for two hardcoded demo users (one per role), as specified
in the Stage 1 plan. Passwords are bcrypt-hashed, never stored in plaintext.
"""
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt, JWTError
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Two demo users. Plaintext passwords shown here only for demo convenience --
# what's actually stored/checked is the bcrypt hash below.
# clerk / clerk123
# manager / manager123
_USERS = {
    "clerk": {
        "user_id": "u_clerk_01",
        "role": "clerk",
        "password_hash": pwd_context.hash("clerk123"),
    },
    "manager": {
        "user_id": "u_manager_01",
        "role": "manager",
        "password_hash": pwd_context.hash("manager123"),
    },
}


def authenticate_user(username: str, password: str):
    """Returns the user dict if credentials are valid, else None."""
    user = _USERS.get(username)
    if not user:
        return None
    if not pwd_context.verify(password, user["password_hash"]):
        return None
    return user


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str):
    """Returns the payload dict if valid, else raises JWTError."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
