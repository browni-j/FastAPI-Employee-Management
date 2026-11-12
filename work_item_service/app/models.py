
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from .database import Base


class WorkItem(Base):
    __tablename__ = "work_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)
    employee_id = Column(Integer, nullable=False, index=True)
    status = Column(String(20), nullable=False, default="TODO")
    priority = Column(String(20), nullable=False, default="MEDIUM")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime,
        server_default=func.now(),
        nullable=False
    )
