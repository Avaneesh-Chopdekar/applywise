from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import init_db
from .logging import configure_logging, LogLevels
from .register_routes import register_routes


configure_logging(LogLevels.info)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


register_routes(app)


@app.get("/api/v1/health-check", tags=["Health Check"])
def health_check():
    return {"status": "ok"}
