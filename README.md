# Employee Management API

A beginner-friendly FastAPI backend application for managing employee records using MySQL and SQLAlchemy.

## Features

* Create a new employee
* View all employees
* View employee by ID
* Update employee details
* Delete an employee
* Health check API
* MySQL database integration
* SQLAlchemy ORM
* Auto-generated employee IDs
* Email validation and normalization
* Case-insensitive duplicate email validation
* Work mode validation (WFH/WFO)
* Employee ID validation
* Proper JSON error handling
* Database transaction rollback on failed changes
* Database session cleanup
* Database persistence across application restarts

## Technologies Used

* Python 3.12
* FastAPI
* Pydantic
* SQLAlchemy
* PyMySQL
* python-dotenv
* Uvicorn
* MySQL 8.0
* Swagger UI
* Git and GitHub

## Project Structure

```text
FastAPI-Employee-Management/
|
|-- app/
|   |-- main.py
|   |-- database.py
|   |-- models.py
|   |-- schemas.py
|   |-- services.py
|
|-- screenshots/
|
|-- .env
|-- .env.example
|-- .gitignore
|-- requirements.txt
|-- README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/browni-j/FastAPI-Employee-Management.git
cd FastAPI-Employee-Management
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
```

### 3. Activate the virtual environment

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell execution policy blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
pip install -r requirements.txt
```

## MySQL Database Setup

Make sure MySQL Server 8.0 is installed and running.

Open MySQL:

```bash
mysql -u root -p
```

Create the database:

```sql
CREATE DATABASE employee_management;
```

Use the database:

```sql
USE employee_management;
```

The application uses SQLAlchemy to create the required `employees` table automatically when the application starts.

To verify the table:

```sql
SHOW TABLES;
```

To view employee records:

```sql
SELECT * FROM employees;
```

## Environment Configuration

Create a `.env` file in the project root.

```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/employee_management
```

Replace `your_password` with the local MySQL password.

A sample configuration is provided in `.env.example`.

The `.env` file is excluded from Git using `.gitignore` and should not be committed to the repository.

## Run the Application

Activate the virtual environment and run:

```powershell
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## Swagger UI

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all available APIs.

## API Endpoints

| Method | Endpoint                   | Description        |
| ------ | -------------------------- | ------------------ |
| GET    | `/health`                  | Health check       |
| POST   | `/employees`               | Create employee    |
| GET    | `/employees`               | Get all employees  |
| GET    | `/employees/{employee_id}` | Get employee by ID |
| PUT    | `/employees/{employee_id}` | Update employee    |
| DELETE | `/employees/{employee_id}` | Delete employee    |

## Employee Fields

| Field           | Description                 |
| --------------- | --------------------------- |
| `id`            | Auto-generated employee ID  |
| `name`          | Employee name               |
| `email`         | Employee email address      |
| `department`    | Employee department         |
| `primary_skill` | Primary technical skill     |
| `location`      | Employee location           |
| `work_mode`     | `WFH` or `WFO`              |
| `is_active`     | Employee active status      |
| `created_at`    | Employee creation timestamp |

## Validation and Error Handling

The application validates:

* Empty or blank employee names
* Invalid email addresses
* Duplicate email addresses
* Case-insensitive duplicate emails
* Invalid work modes
* Invalid employee IDs
* Missing required fields
* Employee not found scenarios

Common responses:

* `201` – Employee created successfully
* `200` – Successful request
* `404` – Employee not found
* `409` – Email already exists
* `422` – Validation error
* `500` – Database operation failure

Database failures return a clear JSON response:

```json
{
  "detail": "Database operation failed"
}
```

Failed database changes are rolled back to prevent incomplete transactions.

## Database Persistence Verification

Database persistence was tested by:

1. Creating employee records.
2. Verifying the records through `GET /employees`.
3. Stopping the FastAPI application.
4. Starting the FastAPI application again.
5. Calling `GET /employees` after restart.
6. Confirming that the previously created records were still available.

The records remained available after restarting the application, confirming that employee data is stored in MySQL rather than an in-memory Python list.

## Testing Evidence

The `screenshots` folder contains API testing and database verification screenshots, including:

* Health check
* Employee creation with HTTP `201`
* Employee listing
* Employee update
* Employee deletion
* Duplicate email validation
* Employee not found
* MySQL database persistence

## Learning Notes

During this task, I learned how to:

* Connect a FastAPI application to MySQL.
* Configure a database connection using environment variables.
* Use SQLAlchemy ORM for database operations.
* Create SQLAlchemy models and map them to database tables.
* Use SQLAlchemy sessions for CRUD operations.
* Handle database transactions and rollbacks.
* Validate request data using Pydantic.
* Handle case-insensitive duplicate email validation.
* Preserve database-generated IDs and creation timestamps.
* Verify that data persists after application restarts.
* Handle database failures with clear JSON responses.
* Organize a FastAPI project into database, model, schema, service, and API layers.

## Challenges and Solutions

### MySQL and SQLAlchemy Integration

Initially, the application used an in-memory Python list. This was replaced with MySQL storage using SQLAlchemy ORM.

### Duplicate Email Handling

Email addresses are normalized to lowercase before checking and storing them. This prevents duplicate accounts using different email letter cases.

### Transaction Handling

Database changes are committed only after successful operations. If a database operation fails, the session is rolled back.

### Persistence

Employee records were verified before and after restarting the FastAPI application to confirm that the data remains stored in MySQL.

### Database Error Handling

A SQLAlchemy exception handler was added to return a clear JSON error message instead of a generic internal server error.

## Conclusion

Task 2 extends the Employee Management API by replacing temporary in-memory storage with persistent MySQL database storage using SQLAlchemy. The application now supports database-backed CRUD operations, validation, transaction handling, error handling, and persistence across application restarts.
