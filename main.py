from fastapi import FastAPI
from app.routes import notes
from app.routes import users

app=FastAPI()
app.include_router(notes.router)
app.include_router(users.router)
