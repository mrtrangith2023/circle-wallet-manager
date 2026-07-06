from fastapi import FastAPI

from app.api.circle import router as circle_router

app = FastAPI(
    title="Circle Wallet Manager API",
    version="0.1.1"
)

app.include_router(circle_router)