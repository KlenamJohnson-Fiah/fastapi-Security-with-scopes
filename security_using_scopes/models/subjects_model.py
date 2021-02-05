from sqlalchemy import Column,String,Integer,ForeignKey,Date,Text

from ..database import Base

class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key = True)
    subject_head = Column(Integer)
    author = Column(String)
    date_of_post = Column(Date)
    synopsis = Column(Text)
    #user_id = Column(Integer)
    user_id = Column(Integer,ForeignKey("users.id"))