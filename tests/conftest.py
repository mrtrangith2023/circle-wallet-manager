import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from app.database.base import Base

from app.main import app

SQLALCHEMY_DATABASE_URL = (
    "sqlite:///:memory:"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,

    connect_args={
        "check_same_thread": False,
    },
)

TestingSessionLocal = sessionmaker(
    autocommit=False,

    autoflush=False,

    bind=engine,
)

@pytest.fixture
def db():

    Base.metadata.create_all(
    bind=engine
)

    db = TestingSessionLocal()

    yield db

    db.close()

    Base.metadata.drop_all(
        bind=engine
    )

    @pytest.fixture
    def client():

        return TestClient(app)