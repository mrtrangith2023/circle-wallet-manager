from fastapi import APIRouter

from app.core.config import settings
from app.services.circle_client import CircleClient

router = APIRouter()

@router.get("/")
def root():
    return {
        "message": "Circle Wallet Manager API is running!"
    }


@router.get("/health")
def health():
    return {
        "status": "healthy"
    }


@router.get("/version")
def version():
    return {
        "version": settings.APP_VERSION
    }


@router.get("/config")
def config():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG
    }


@router.get("/client")
def client_info():
    client = CircleClient()

    return {
        "base_url": client.base_url,
        "environment": settings.ENVIRONMENT
    }


@router.get("/info")
def info():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT
    }