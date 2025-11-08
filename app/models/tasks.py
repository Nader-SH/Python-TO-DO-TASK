from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.db.base import Base

class Tasks(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=False)
    completed = Column(Boolean, default=False)
