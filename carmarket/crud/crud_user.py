from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from carmarket.utils.security import gen_password_hash, verify_password
from carmarket.crud.base import CRUDBase
from carmarket.models import User
from carmarket.schemas import UserCreate


class CRUDUser(CRUDBase[User, UserCreate]):
    def get_by_email_or_phone(self, db: Session, *, email: str, phone_number: str) -> Optional[User]:
        stmt = select(User).where(or_(User.email == email, User.phone_number == phone_number))
        return db.execute(stmt).scalar_one_or_none()

    def create(self, db: Session, *, user_info: UserCreate) -> User:
        user = User(
            phone_number=user_info.phone_number,
            email=user_info.email,
            hashed_password=gen_password_hash(user_info.password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def authenticate(self, db: Session, *, email: str, phone_number: str, password: str) -> Optional[User]:
        user = self.get_by_email_or_phone(db, email=email, phone_number=phone_number)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
