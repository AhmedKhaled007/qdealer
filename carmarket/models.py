
from typing import List, Optional
from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP, func, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from uuid import UUID


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    phone_number: Mapped[str] = mapped_column(String, index=True, unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    created_at_utc: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True),  nullable=False, server_default=func.now())
    updated_at_utc: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(),  onupdate=func.now())

    car_ads: Mapped[List["CarAd"]] = relationship("CarAd", back_populates="owner")


class CarAd(Base):
    __tablename__ = "car_ads"
    id = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    brand: Mapped[str] = mapped_column(String, nullable=False)
    model: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    kilometers: Mapped[Optional[str]] = mapped_column(Integer, nullable=True)
    price: Mapped[float] = mapped_column(Float(precision=2), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["User"] = relationship(back_populates="car_ads")
    images: Mapped[List["Image"]] = relationship(back_populates="car_ad")


class Image(Base):
    __tablename__ = "images"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    uuid: Mapped[UUID] = mapped_column('uuid', PGUUID(as_uuid=True), nullable=False, unique=True)
    img_path: Mapped[str] = mapped_column(String, nullable=False)
    car_ad_id: Mapped[int] = mapped_column(ForeignKey("car_ads.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    car_ad: Mapped["CarAd"] = relationship(back_populates="images")
