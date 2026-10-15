from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Literal
from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request, Response

from app.database import Base, engine, get_db
from app.models import Employee, WorkItem
from app.schemas import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeListResponse,
    EmployeeUpdate,
)
from app.schemas import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeListResponse,
    EmployeeUpdate,
    WorkItemCreate,
    WorkItemResponse,
    WorkItemListResponse,
    WorkItemUpdate,
    WorkItemStatusUpdate,
)
from app.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
    create_work_item,
    get_all_work_items,
    get_work_item_by_id,
    update_work_item,
    update_work_item_status,
    delete_work_item,
    get_employee_work_summary,
)

app = FastAPI()

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed"}
    )

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    created_employee = create_employee(db, employee)

    if created_employee == "duplicate_email":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return created_employee


@app.get("/employees", response_model=EmployeeListResponse)
def get_employees(
    search: str | None = Query(default=None),
    department: str | None = Query(default=None),
    work_mode: str | None = Query(default=None, pattern="^(WFH|WFO)$"),
    is_active: bool | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return get_all_employees(
        db=db,
        search=search,
        department=department,
        work_mode=work_mode,
        is_active=is_active,
        limit=limit,
        offset=offset,
    )


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee



@app.get("/employees/{employee_id}/work-summary")
def get_employee_work_summary_endpoint(
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    summary = get_employee_work_summary(db, employee_id)

    return {
        "employee_id": employee.id,
        "employee_name": employee.name,
        **summary,
    }


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def edit_employee(
    employee: EmployeeUpdate,
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    updated_employee = update_employee(db, employee_id, employee)

    if updated_employee == "duplicate_email":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    if updated_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return updated_employee

@app.delete("/employees/{employee_id}", response_model=str)
def remove_employee(
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    deleted_employee = delete_employee(db, employee_id)

    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if deleted_employee == "has_work_items":
        raise HTTPException(
            status_code=400,
            detail="Cannot delete employee with assigned work items. Reassign or delete the work items first."
        )

    return "Employee deleted successfully"

@app.post(
    "/work-items",
    response_model=WorkItemResponse,
    status_code=201
)
def add_work_item(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):
    created_work_item = create_work_item(db, work_item)

    if created_work_item == "employee_not_found":
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if created_work_item == "invalid_initial_status":
        raise HTTPException(
            status_code=400,
            detail="New work item must have TODO status"
        )

    return created_work_item

@app.get(
    "/work-items",
    response_model=WorkItemListResponse
)
def get_work_items(
    search: str | None = Query(default=None),
    employee_id: int | None = Query(default=None, gt=0),
    status: Literal["TODO", "IN_PROGRESS", "COMPLETED"] | None = Query(default=None),
    priority: Literal["LOW", "MEDIUM", "HIGH"] | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    return get_all_work_items(
        db=db,
        search=search,
        employee_id=employee_id,
        status=status,
        priority=priority,
        limit=limit,
        offset=offset,
    )

@app.get(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def get_work_item(
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    work_item = get_work_item_by_id(db, work_item_id)

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return work_item

@app.put(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def edit_work_item(
    work_item: WorkItemUpdate,
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    updated_work_item = update_work_item(
        db,
        work_item_id,
        work_item
    )
    if updated_work_item == "invalid_status_transition":
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition",
        )

    if updated_work_item == "employee_not_found":
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if updated_work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return updated_work_item

@app.patch(
    "/work-items/{work_item_id}/status",
    response_model=WorkItemResponse,
)
def edit_work_item_status(
    status_update: WorkItemStatusUpdate,
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db),
):
    updated_work_item = update_work_item_status(
        db,
        work_item_id,
        status_update,
    )

    if updated_work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found",
        )

    if isinstance(updated_work_item, str):
        raise HTTPException(
            status_code=400,
            detail="Invalid status transition",
        )

    return updated_work_item


@app.delete(
    "/work-items/{work_item_id}",
    status_code=204
)
def remove_work_item(
    work_item_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    deleted = delete_work_item(db, work_item_id)

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return Response(status_code=204)


