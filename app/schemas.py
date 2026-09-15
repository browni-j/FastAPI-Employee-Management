from datetime import datetime
from typing import Literal

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