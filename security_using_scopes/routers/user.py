from fastapi import APIRouter,Depends,status,HTTPException,Security
from typing import List
from fastapi.responses import JSONResponse

from datetime import timedelta




from ..schemas import subject_schema,users_schema,token_schema
from ..models import scopes_model,subjects_model,users_model
from ..cruds import crud
from ..dependencies import oauth2,password_hashing


from ..database import SessionLocal,engine
from sqlalchemy.orm import Session

users_model.Base.metadata.create_all(bind=engine)

router = APIRouter(
    prefix= "/user",
    tags = ["user"],


)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/new_user/")#response_model= users_schema.CreateUser
async def create_user(user:users_schema.CreateUser, db:Session = Depends(get_db)):
    checker = crud.email_check(db=db, email=user.email)
    if checker == None:
        encrypted_password = password_hashing.hash_password(user.password)
        final_detail = {**user.dict(), "password" : encrypted_password}
        db_newUser = crud.put_new_user(db=db,user= final_detail)
        return HTTPException(status.HTTP_201_CREATED, detail="user created", headers= {"X-User_Created":"usercreated"})
    raise HTTPException(status.HTTP_409_CONFLICT, detail="user already exist")

@router.post("/token/",response_model=token_schema.Token)
async def login_user(form_data: oauth2.OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    get_object_from_db = crud.get_user_info(db=db, email=form_data.username)
    if get_object_from_db == None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="No user found with credentials")
    if password_hashing.verify_password(form_data.password,get_object_from_db.password) == True:
        raise HTTPException(status.HTTP_202_ACCEPTED,detail="password was checked right")
    access_token_expires = timedelta(minutes=password_hashing.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth2.create_access_token(data={"sub": get_object_from_db.email,"scopes": form_data.scope.id}, expires_delta=access_token_expires)
    #print(access_token)
    return{"access_token": access_token, "token_type": "bearer"}
    
    """
    else:
        raise HTTPException(status.HTTP_203_NON_AUTHORITATIVE_INFORMATION, detail="password was wrong")
    """
@router.get("/me/articles/")
async def read_all_articles(articles:List[subject_schema.Subject]= Security(scopes=["me"]),db:Session = Depends(get_db)):
    all_articles_in_db = crud.get_all_articles(db=db)
    return JSONResponse(content=all_articles_in_db)

@router.get("/users/me/")
async def read_users_me(current_user: users_schema.User = Depends(oauth2.get_user_scope)):
    return current_user