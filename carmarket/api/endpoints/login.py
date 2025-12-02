from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from carmarket.api import dependency
from carmarket.utils import security
from carmarket.utils.config import settings
from carmarket.utils.security import gen_password_hash
from carmarket import crud, models, schemas

router = APIRouter()


@router.post("/login")
def login_access_token(
    form_data: schemas.LoginForm, db: Session = Depends(dependency.get_db)
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.email, password=form_data.password, phone_number=form_data.phone_number
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.User)
def create_user(user_info: schemas.UserCreate,
                db: Session = Depends(dependency.get_db)
                ) -> Any:
    """
    Create register new user 
    """
    user = crud.user.get_by_email_or_phone(db, email=user_info.email, phone_number=user_info.phone_number)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email or phone_number already exists in the system",
        )
    user = crud.user.create(db, user_info=user_info)

    return schemas.User.from_orm(user)
