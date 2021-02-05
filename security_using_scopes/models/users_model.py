from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .scopes_model import Scope

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key = True)
    name = Column(String)
    email = Column(String)
    prefered_username = Column(String)
    password = Column(String)
    scope_id = Column(Integer, ForeignKey("scopes.id"))
    scope = relationship("Scope",back_populates="user")