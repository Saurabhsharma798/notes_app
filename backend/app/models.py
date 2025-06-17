from sqlalchemy import String,Integer,Column,ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base=declarative_base()

class USER(Base):
    __tablename__ = 'users'
    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,index=True)
    hashed_password=Column(String)

class NOTE(Base):
    __tablename__ = "notes"

    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,index=True)
    content=Column(String)
    owner_id=Column(Integer,ForeignKey('users.id'))


    
