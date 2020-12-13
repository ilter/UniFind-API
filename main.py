from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from apps.school.routers import router as school_router

app = FastAPI()

app.include_router(school_router, tags=["Schools"], prefix="/schools")


@app.on_event("startup")
async def connect_db():
    app.mongodb_client = AsyncIOMotorClient()
    app.mongodb = app.mongodb_client[]


@app.on_event("shutdown")
async def startup_db():
    app.mongodb_client.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port="5555",
    )
