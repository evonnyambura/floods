from fastapi import FastAPI


from app.models.user import User
from app.models.location import Location
from database import Base, engine

from app.routers.user import router as user_router
from app.routers.auth import router as auth_router
from app.routers.location import router as location_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Flood API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(location_router)


@app.get("/")
def root():
    return {
        "message": "Flood Monitoring API is running"
    }