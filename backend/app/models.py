from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.database import Base


class Task(Base):

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)

    category = Column(String)

    estimated_hours = Column(Integer)

    deadline = Column(String)

    priority_score = Column(Integer, default=0)

    completed = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)