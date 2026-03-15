from contextlib import asynccontextmanager

from fastapi import FastAPI

import models
from db import Base, engine
from routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello to you."}

app.include_router(router, prefix="/api")
