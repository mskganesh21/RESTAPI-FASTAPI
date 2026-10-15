import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.database import engine
from app.middleware.logging import RequestLoggingMiddleware
from app.routers import notes

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="Notes API",
    description="Phase 0.3 - FastAPI CRUD API with PostgreSQL",
    version="0.3.0",
    lifespan=lifespan,
)

app.add_middleware(RequestLoggingMiddleware)
app.include_router(notes.router)


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "message": "Notes API is running",
        "docs": "/docs",
        "notes": "/notes",
    }


@app.get("/health")
async def health() -> dict[str, str]:
    async with engine.connect() as connection:
        await connection.execute(text("SELECT 1"))
    return {"status": "ok", "database": "connected"}
