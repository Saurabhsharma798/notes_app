from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models import USER


pwd_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
secret_key="abcd"
ALGORITHM="HS256"
ACCESS_TOKEN_EXP_MIN=30
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')



def hash_password(password:str)->str:
    return pwd_context.hash(password)


def verify_password(plain_password:str,hash_password:str)->bool:
    return pwd_context.verify(plain_password,hash_password)


def create_access_token(data:dict,expire_delta:timedelta=None):
    to_encode=data.copy()
    expire=datetime.now() + (expire_delta or timedelta(minutes=ACCESS_TOKEN_EXP_MIN))
    to_encode.update({'exp':expire})
    return jwt.encode(to_encode,secret_key,algorithm=ALGORITHM)
    

def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    credentials_exception=HTTPException(
        status_code=401,
        detail="could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )

    try:
        payload=jwt.decode(token,secret_key,algorithms=ALGORITHM)
        username:str=payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception


    user=db.query(USER).filter(USER.username==username).first()
    if user is None:
        raise credentials_exception
    
    return user

