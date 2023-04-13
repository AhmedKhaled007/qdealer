from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
import phonenumbers
from uuid import UUID


class Login(BaseModel):
    username: str
    password: str


class TokenPayload(BaseModel):
    sub: int


class UserCreate(BaseModel):
    email: Optional[EmailStr]
    phone_number: str
    password: str

    @validator('phone_number')
    def validate_phone(cls, v) -> str:
        try:
            phone_number = phonenumbers.parse(v)
        except phonenumbers.phonenumberutil.NumberParseException as e:
            raise ValueError('Invalid phone format', str(e))
        if not phonenumbers.is_valid_number(phone_number):
            raise ValueError('Invalid phone number')

        return v


class LoginForm(BaseModel):
    phone_number: Optional[str]
    password: str
    email: Optional[EmailStr]

    @validator('email', always=True)
    def validate_email_or_phone_exist(cls, v, values) -> str:
        if not v and not values.get('phone_number'):
            raise ValueError('email or phone_number required')
        return v


class User(BaseModel):
    email: Optional[str]
    phone_number: str

    class Config:
        orm_mode = True


class Image(BaseModel):
    uuid: UUID

    class Config:
        orm_mode = True


class CarAdCreate(BaseModel):
    title: str
    brand: str
    model: str
    year: int
    kilometers: Optional[int]
    price: float


class CarAd(BaseModel):
    title: str
    brand: str
    model: str
    year: int
    kilometers: Optional[int]
    price: float
    images: List['Image']

    class Config:
        orm_mode = True
