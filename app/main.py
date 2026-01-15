from fastapi import FastAPI

from app.database import engine, Base
from app.routers import health

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Synergy Way Test Task",
    description="API for fetching and managing users, posts and comments",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(health.router)


@app.get("/")
def root():
    return {"message": "Synergy Way Test Task API"}
