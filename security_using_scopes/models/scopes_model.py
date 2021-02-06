
"""
from sqlalchemy import Column,String,Integer,ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Scope(Base):
    __tablename__ = "scopes"

    id = Column(Integer, primary_key = True)
    scope = Column(String)
    #user_id = Column(Integer,ForeignKey("users.id"))
    user = relationship("User",back_populates="scope")

"""