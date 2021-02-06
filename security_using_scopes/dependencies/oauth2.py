from fastapi import Depends,Security,HTTPException,status
from fastapi.security import (OAuth2PasswordBearer,OAuth2PasswordRequestForm,SecurityScopes)
from typing import List,Optional
from datetime import datetime, timedelta
from ..schemas.users_schema import LoginUser,User
from .password_hashing import verify_password,SECRET_KEY,ALGORITHM
from jose import JWTError,jwt
from ..cruds import crud

from pydantic import ValidationError

from sqlalchemy.orm import Session
from ..database import SessionLocal,engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/token",
    #scopes={"me": "Read information about the current user.", "items": "Read items."}
)

async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(security_scopes:SecurityScopes, token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},)

    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = crud.username_check(db=db,username=username)
    if user is None:
        print("no username")
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
            
    return user

    

async def get_user_scope(user_scope: User = Security(get_current_user,scopes=["user:r"])):
    if user_scope.scope != "user:r":
        raise HTTPException(status_code= 400, detail="mot user:read")
    return user_scope