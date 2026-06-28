from fastapi import FastAPI

app = FastAPI(
    title="Circle Wallet Manager API",
    version="0.1.1"
)

@app.get("/")
def root():
    return {
        "message": "Circle Wallet Manager API is running!"
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