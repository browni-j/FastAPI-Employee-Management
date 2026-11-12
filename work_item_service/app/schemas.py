
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WorkItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    employee_id: int
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None


class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    employee_id: int
    status: str
    priority: str
    due_date: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
