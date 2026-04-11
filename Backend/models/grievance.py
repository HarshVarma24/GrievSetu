from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from database.database import Base
import datetime

class Grievance(Base):
    __tablename__ = "grievances"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String(500), nullable=False)
    image_path = Column(String(500))
    category = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    priority = Column(String(50), nullable=False)
    department = Column(String(50), nullable=False)

    created_at = Column(DateTime, default=datetime.datetime.now)
    

    
