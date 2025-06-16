from fastapi import FastAPI
from app.routes import notes

app=FastAPI()
app.include_router(notes.router)
