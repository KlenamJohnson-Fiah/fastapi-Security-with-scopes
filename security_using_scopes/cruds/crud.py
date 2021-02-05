from sqlalchemy.orm import Session

from ..models import subjects_model,users_model
from ..schemas import users_schema,subject_schema

def get_all_articles(db:Session)->dict:
    return db.query(subjects_model.Subject).all()

def get_article_by_specific_author(db:Session, author_name:str)->dict:
    return db.query(subjects_model.Subject).filter(subject_models.author == author_name).all()

def get_article_by_word_Subject(db:Session, word: str)->dict:
    search = f"%{word}%"
    subject_check = db.query(subjects_model.Subject).filter(subjects_model.subject_head.like(search)).all()
    return subject_check

def get_article_by_word_Synopsis(db:Session, word:str)->dict:
    search = f"%{word}%"
    synopsis_check = db.query(subjects_model.Subject).filter(subjects_model.synopsis.like(search)).all()
    return synopsis_check

def put_new_user(db:Session, user:users_schema.CreateUser)->dict:
    db_user = users_model.User(**user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def username_check(db:Session, username:str)->dict:
    checker = db.query(users_model.User).filter(users_model.User.name == username).first()
    return checker

def get_user_info(db:Session, email:str)->dict:
    user_info_query = db.query(users_model.User).filter(users_model.User.email == email).first()
    return user_info_query