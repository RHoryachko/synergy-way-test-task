from fastapi import FastAPI

from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Synergy Way Test Task")


@app.get("/")
def root():
    return {"message": "Synergy Way Test Task API"}
