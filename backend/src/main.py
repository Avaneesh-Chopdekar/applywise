from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import init_db
from .logging import configure_logging, LogLevels


configure_logging(LogLevels.info)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/api/v1/health-check")
def health_check():
    return {"status": "ok"}
