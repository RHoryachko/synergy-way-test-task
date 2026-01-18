import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine, Base
from app.routers import health, users, posts, comments
from app.logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    try:
        Base.metadata.create_all(bind=engine, checkfirst=True)
    except Exception as e:
        logger.warning(f"Tables may already exist: {e}")
    yield
    logger.info("Application shutdown")


app = FastAPI(
    title="Synergy Way Test Task",
    description="API for fetching and managing users, posts and comments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(health.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/")
def root():
    return {"message": "Synergy Way Test Task API"}
