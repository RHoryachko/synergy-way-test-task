from fastapi import FastAPI

app = FastAPI(title="Synergy Way Test Task")


@app.get("/")
def root():
    return {"message": "Synergy Way Test Task API"}
