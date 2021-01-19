from fastapi import FastAPI
import uvicorn
from database import Database
from apps.school.routers import router as school_router
from apps.auth.routers import router as auth_router

# App & MongoDB
app = FastAPI()
database = Database()

# Routes
app.include_router(school_router, tags=["Schools"], prefix="/schools")
app.include_router(auth_router, tags=["auth"])

@app.on_event("startup")
async def connect_db():
    if database.connect_db() is not None:
        print("Connection okey!")
    else:
        print("Connection not okey")


@app.on_event("shutdown")
async def startup_db():
    database.close_db()


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info", reload=True)
