import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
import jwt

from app.model.usuario import Usuario

key = os.getenv("JWT_KEY")

application_token_scheme = HTTPBearer(scheme_name="Token")


def get_current_user(token: HTTPAuthorizationCredentials = Depends(application_token_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, key, algorithms=["HS256"])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception
        user = payload
    except Exception:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Usuario = Depends(get_current_user)):
    return current_user
