from pydantic import BaseModel,EmailStr
from typing import Optional

class User(BaseModel):
    name : str
    scope : str

    class Config:
        orm_mode = True


class LoginUser(User):
    password : str



class CreateUser(LoginUser):
    email : EmailStr
    prefered_username : str

    class Config:
        orm_mode = True

  

