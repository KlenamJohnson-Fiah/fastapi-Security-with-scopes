from pydantic import BaseModel

class Subject(BaseModel):
    synopsis : str
    author : str
    date_of_post : str
    subject_head : str
    

    class Config():
        orm_mode = True

class Create_newSubject(Subject):
    pass

