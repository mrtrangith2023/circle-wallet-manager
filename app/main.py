from fastapi import FastAPI
from app.models.wallet import Wallet
from app.api.circle import router as circle_router
from app.api.wallet import router as wallet_router

from app.core.logger import logger
from app.core.handlers import register_exception_handlers
from app.core.middleware import log_requests
from app.api.auth import (
    router as auth_router,
)
from app.api.user import (
    router as user_router,
)

app = FastAPI(
    title="Circle Wallet Manager API",
    version="0.1.1"
)

app.middleware("http")(log_requests)

register_exception_handlers(app)

app.include_router(circle_router)
app.include_router(wallet_router)
app.include_router(user_router)
app.include_router(auth_router)