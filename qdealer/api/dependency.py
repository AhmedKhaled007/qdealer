from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from qdealer import crud, models, schemas
from qdealer.utils import security
from qdealer.utils.config import settings
from qdealer.db import SessionLocal


bearer_schema: HTTPBearer = HTTPBearer(bearerFormat="JWT", scheme_name="JWT Bearer")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: HTTPAuthorizationCredentials = Depends(bearer_schema)
) -> models.User:
    try:
        payload = jwt.decode(
            token.credentials, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.DecodeError, ValidationError) as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
