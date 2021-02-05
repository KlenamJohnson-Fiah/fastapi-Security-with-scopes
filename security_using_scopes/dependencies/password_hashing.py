from passlib.context import CryptContext

SECRET_KEY = "c230e3fb378cff88f724cb56cab3a0a331acc3259d2f93c8703e7aa0190aff34"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")


def hash_password(password)->str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password)->bool:
    pass_check = pwd_context.verify(plain_password,hashed_password)
    return True