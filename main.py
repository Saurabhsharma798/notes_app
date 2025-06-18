from fastapi import FastAPI
from app.routes import notes
from app.routes import users
from dotenv import load_dotenv

load_dotenv()


app=FastAPI()
@app.get('/')
def home():
    return {'message':"you entered the home page"}
app.include_router(notes.router)
app.include_router(users.router)
