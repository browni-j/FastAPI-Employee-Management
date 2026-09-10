# Employee Management API

A beginner-friendly FastAPI backend application for managing employee records using an in-memory Python list.

## Features

* Create a new employee
* View all employees
* View employee by ID
* Update employee details
* Delete an employee
* Health check API
* Email validation
* Duplicate email validation
* Work mode validation (WFH/WFO)
* Employee ID validation
* Proper error handling

## Technologies Used

* Python 3.12
* FastAPI
* Pydantic
* Uvicorn
* Swagger UI
* Git

## Project Structure

```text
Stackly_task/
│
├── app/
│   ├── main.py
│   ├── schemas.py
│   └── services.py
│
├── requirements.txt
└── README.md
```

## Setup

### 1. Create and activate virtual environment

```powershell
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Run the application

```powershell
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## Swagger Documentation

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all the APIs.

## API Endpoints

| Method | Endpoint          | Description              |
| ------ | ----------------- | ------------------------ |
| GET    | `/health`         | Check application health |
| POST   | `/employees`      | Create employee          |
| GET    | `/employees`      | Get all employees        |
| GET    | `/employees/{id}` | Get employee by ID       |
| PUT    | `/employees/{id}` | Update employee          |
| DELETE | `/employees/{id}` | Delete employee          |

## Employee Fields

Each employee contains:

* `id` – Auto-generated employee ID
* `name` – Employee name
* `email` – Valid and unique email address
* `department` – Employee department
* `primary_skill` – Primary technical skill
* `location` – Employee location
* `work_mode` – WFH or WFO
* `is_active` – Employee active status
* `created_at` – Employee creation date and time

## Validation

The application validates:

* Required employee fields
* Valid email format
* Unique email address
* Work mode must be `WFH` or `WFO`
* Employee ID must be greater than 0
* Employee not found returns `404`
* Duplicate email returns `409`
* Invalid request data returns `422`

## What I Learned

* FastAPI application structure
* Creating REST APIs
* CRUD operations
* Pydantic data validation
* Path parameter validation
* HTTP status codes
* Error handling using `HTTPException`
* Using Swagger UI for API testing
* Working with virtual environments
* Managing Python dependencies using `requirements.txt`

## Difficulties Faced

* Understanding FastAPI project structure
* Implementing CRUD operations using a Python list
* Handling duplicate email validation
* Implementing proper `404` and `409` error responses
* Understanding Pydantic validation errors
* Working with virtual environments and dependencies

## Assumptions

* Employee data is stored temporarily in a Python list.
* Data will be lost when the application restarts.
* No database or authentication is required for this assignment.
* Employee IDs are generated automatically.

## Conclusion

This project demonstrates a basic employee management REST API using FastAPI with CRUD operations, input validation, and proper error handling.
