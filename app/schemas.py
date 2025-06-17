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
        from_attributes = True


class NotesCreate(BaseModel):
    title:str
    content:str

class NotesOut(BaseModel):
    id:int
    title:str
    content:str


    class Config():
        from_attributes = True

        
class NotesUpdate(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None

class Token(BaseModel):
    access_token: str
    token_type: str
