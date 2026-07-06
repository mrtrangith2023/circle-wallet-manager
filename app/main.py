from fastapi import FastAPI
from app.database.database import engine
from app.database.base import Base
from app.models.wallet import Wallet
from app.api.circle import router as circle_router

app = FastAPI(
    title="Circle Wallet Manager API",
    version="0.1.1"
)

Base.metadata.create_all(bind=engine)

app.include_router(circle_router)