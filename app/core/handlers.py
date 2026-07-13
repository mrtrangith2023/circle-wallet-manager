from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime
from app.core.exceptions import AppException

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request,
        exc: AppException,
    ):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "error": exc.__class__.__name__,
                "message": exc.detail,
                "path": request.url.path,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            },
        )