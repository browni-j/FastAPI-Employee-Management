from fastapi import FastAPI, HTTPException, Path
from app.schemas import EmployeeCreate
from app.services import create_employee, get_all_employees, get_employee_by_id, update_employee, delete_employee

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/employees", status_code=202)
def add_employee(employee: EmployeeCreate):
    created_employee = create_employee(employee)

    if created_employee is None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return created_employee

@app.get("/employees")
def get_employees():
    return get_all_employees()

@app.get("/employees/{employee_id}")
def get_employee(employee_id: int = Path(gt=0)):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee

@app.put("/employees/{employee_id}")
def edit_employee(
    employee: EmployeeCreate,
    employee_id: int = Path(gt=0)
):
    updated_employee = update_employee(employee_id, employee)

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


@app.delete("/employees/{employee_id}")
def delete_employee_api(employee_id: int = Path(gt=0)):
    deleted_employee = delete_employee(employee_id)

    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully",
        "employee": deleted_employee
    }
