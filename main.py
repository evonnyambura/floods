from fastapi import FastAPI

from app.routers.user import router as user_router
from app.routers.auth import router as auth_router


app = FastAPI(
    title="flood API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(auth_router)


@app.on_event("startup")
def startup_message():
    print("\n" + "=" * 50)
    print("Flood Monitoring API is running")
    print("API:     http://127.0.0.1:8000")
    print("Swagger: http://127.0.0.1:8000/docs")
    print("ReDoc:   http://127.0.0.1:8000/redoc")
    print("=" * 50 + "\n")


@app.get("/")
def root():
    return {
        "message": "Flood Monitoring API is running"
    }