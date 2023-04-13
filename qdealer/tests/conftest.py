import os
import pytest
from typing import Generator, Callable

from qdealer.utils.config import settings
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Engine, create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from alembic.config import Config
from alembic import command


@pytest.fixture
def setup_db() -> Engine:
    url = f"{settings.SQLALCHEMY_DATABASE_URI}_test"
    if database_exists(url):
        drop_database(url)
    create_database(url)
    yield url
    drop_database(url)


@pytest.fixture(autouse=True)
def setup_migration(setup_db):
    os.environ["TESTING"] = "True"
    config = Config("/app/alembic.ini")
    config.set_main_option("sqlalchemy.url", setup_db)
    config.set_main_option('script_location', '/app/alembic')
    command.upgrade(config, "head")
    yield setup_db


@pytest.fixture
def engine(setup_migration: str) -> Engine:
    engine = create_engine(setup_migration)
    yield engine
    engine.dispose()


@pytest.fixture
def session_factory(engine) -> Generator[Session, None, None]:
    yield sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_dependency(session_factory) -> Callable:
    def test_db():
        db = session_factory()
        try:
            yield db
        finally:
            db.close()
    return test_db


@pytest.fixture
def session(session_factory) -> Session:
    session = session_factory()
    yield session
    session.close()
