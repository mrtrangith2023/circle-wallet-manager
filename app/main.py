from fastapi import FastAPI
from app.core.config import settings
from app.services.circle_client import CircleClient

app = FastAPI(
    title="Circle Wallet Manager API",
    version="0.1.1"
)

@app.get("/")
def root():
    return {
        "message": "Circle Wallet Manager API is running!"
    }

@app.get("/config")
def config():

    return {

        "app": settings.APP_NAME,

        "version": settings.APP_VERSION,

        "debug": settings.DEBUG

    }

@app.get("/health")
def health():
    return {
        "status" : "healthy"
    }

@app.get("/version")
def version():
    return {
        "version" : "0.1.1"
    }

@app.get("/client")

def client_info():

    client = CircleClient()

    return {

        "base_url": client.base_url

    }