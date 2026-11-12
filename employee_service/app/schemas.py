from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: str
    is_active: bool = True


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)