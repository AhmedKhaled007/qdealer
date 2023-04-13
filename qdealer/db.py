from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from qdealer.utils.config import settings


SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal: sessionmaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
