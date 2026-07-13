from fastapi import FastAPI
from app.models.wallet import Wallet
from app.api.circle import router as circle_router
from app.api.wallet import router as wallet_router

from app.core.logger import logger
from app.core.handlers import register_exception_handlers
from app.core.middleware import log_requests

app = FastAPI(
    title="Circle Wallet Manager API",
    version="0.1.1"
)

app.middleware("http")(log_requests)

register_exception_handlers(app)

app.include_router(circle_router)
app.include_router(wallet_router)