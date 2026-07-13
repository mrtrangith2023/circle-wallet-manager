from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# DATABASE_URL = "sqlite:///./circle.db"
DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)