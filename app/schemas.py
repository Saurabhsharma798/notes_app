from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username:str
    password:str

class UserLogin(BaseModel):
    username:str
    password:str

class UserOut(BaseModel):
    id:int
    username:str

    class Config():
        orm_mode=True


class NotesCreate(BaseModel):
    title:str
    content:str

class NotesOut(BaseModel):
    id:int
    title:str
    content:str


    class Config():
        orm_mode=True

        
class NotesUpdate(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None