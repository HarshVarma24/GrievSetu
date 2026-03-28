from sqlalchemy import Column, Integer, String, Enum
from database.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(100))
    email = Column(String(100), unique = True, index = True)
    password = Column(String(250))
    role = Column(Enum("citizen", "admin"), default = "citizen")