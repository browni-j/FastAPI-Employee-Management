from pydantic import BaseModel, EmailStr, Field
from typing import Literal
from datetime import datetime


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: Literal["WFH", "WFO"]
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)

    