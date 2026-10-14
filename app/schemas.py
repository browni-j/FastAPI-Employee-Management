from datetime import datetime
from typing import Literal
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmployeeBase(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: Literal["WFH", "WFO"]
    is_active: bool = True

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def reject_blank(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Field cannot be blank")

        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str):
        return value.strip().lower()


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class EmployeeResponse(EmployeeBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    

class EmployeeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[EmployeeResponse]


class WorkItemCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    employee_id: int = Field(gt=0)
    status: str = "TODO"
    priority: Literal["LOW", "MEDIUM", "HIGH"] = "MEDIUM"
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def reject_blank_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")
        
        return value


class WorkItemUpdate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    employee_id: int = Field(gt=0)
    status: Literal["TODO", "IN_PROGRESS", "COMPLETED"] | None = None
    priority: Literal["LOW", "MEDIUM", "HIGH"]
    due_date: date | None = None

    @field_validator("title")
    @classmethod
    def reject_blank_title(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Title cannot be blank")
        
        return value

    @field_validator("status", mode="before")
    @classmethod
    def reject_null_status(cls, value):
        if value is None:
            raise ValueError("Status cannot be null")
        return value


class WorkItemStatusUpdate(BaseModel):
    status: Literal["TODO", "IN_PROGRESS", "COMPLETED"]


class AssignedEmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: str | None
    employee_id: int
    status: str
    priority: str
    due_date: date | None
    created_at: datetime
    assigned_employee: AssignedEmployeeResponse

    model_config = ConfigDict(from_attributes=True)


class WorkItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[WorkItemResponse]