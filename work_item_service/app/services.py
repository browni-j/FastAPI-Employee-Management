
import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException

from .models import WorkItem
from .schemas import WorkItemCreate


EMPLOYEE_SERVICE_URL = "http://127.0.0.1:8001"


def validate_employee(employee_id: int):
    try:
        response = httpx.get(
            f"{EMPLOYEE_SERVICE_URL}/employees/{employee_id}",
            timeout=5.0
        )

        if response.status_code == 404:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        response.raise_for_status()

    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=503,
            detail="Employee Service unavailable"
        ) from exc

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=503,
            detail="Employee Service unavailable"
        ) from exc


def create_work_item(db: Session, work_item: WorkItemCreate):
    validate_employee(work_item.employee_id)

    db_work_item = WorkItem(
        title=work_item.title,
        description=work_item.description,
        employee_id=work_item.employee_id,
        status=work_item.status,
        priority=work_item.priority,
        due_date=work_item.due_date
    )

    db.add(db_work_item)
    db.commit()
    db.refresh(db_work_item)

    return db_work_item


def get_work_items(db: Session):
    return db.query(WorkItem).order_by(WorkItem.id).all()


def get_work_item_by_id(db: Session, work_item_id: int):
    return db.query(WorkItem).filter(
        WorkItem.id == work_item_id
    ).first()
