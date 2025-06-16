from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from models import USER
from database import get_db
from schemas import UserCreate,UserOut,UserLogin
from auth import hash_password,verify_password,create_access_token


router=APIRouter(
    tags=['Auth']
)

@router.post("/register",response_model=UserOut)
def register(user:UserCreate,db:Session=Depends(get_db)):
    hashed=hash_password(user.password)
    new_user=USER(username=user.username,hash_password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    db_user=db.query(USER).filter(USER.username==user.username).first()
    if not db_user or not verify_password(user.password,db_user.hashed_password):
        raise HTTPException(status_code=400,detail="invalid credentials")
    
    access_token=create_access_token(data={"sub":db_user.username})

    return {'access_token':access_token,"token_type":"bearer"}