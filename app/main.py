from fastapi import FastAPI

app = FastAPI(
    title="Circle Wallet Manager",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Circle Wallet Manager API is running!"
    }