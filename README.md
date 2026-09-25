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
* Work mode validation (`WFH`/`WFO`)
* Employee ID validation
* Proper JSON error handling
* Database transaction rollback on failed changes
* Database session cleanup
* Database persistence across application restarts
* Employee search by name
* Department filtering
* Work mode filtering
* Active/inactive employee filtering
* Combined filters
* Pagination using limit and offset
* Employee listing ordered by ID

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

### 1. Clone the Repository

```bash
git clone https://github.com/browni-j/FastAPI-Employee-Management.git
cd FastAPI-Employee-Management
```

### 2. Switch to the Task 3 Branch

```bash
git switch task-3
```

### 3. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

### 4. Activate the Virtual Environment

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

### 5. Install Dependencies

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

| Method | Endpoint                   | Description                                                |
| ------ | -------------------------- | ---------------------------------------------------------- |
| GET    | `/health`                  | Health check                                               |
| POST   | `/employees`               | Create employee                                            |
| GET    | `/employees`               | Get employees with optional search, filters and pagination |
| GET    | `/employees/{employee_id}` | Get employee by ID                                         |
| PUT    | `/employees/{employee_id}` | Update employee                                            |
| DELETE | `/employees/{employee_id}` | Delete employee                                            |

## Employee Fields

| Field           | Description                |
| --------------- | -------------------------- |
| `id`            | Auto-generated employee ID |
| `name`          | Employee name              |
| `email`         | Employee email address     |
| `department`    | Employee department        |
| `primary_skill` | Primary technical skill    |
| `location`      | Employee work location     |
| `work_mode`     | `WFH` or `WFO`             |
| `is_active`     | Employee active status     |
| `created_at`    | Record creation timestamp  |

## Task 3 - Search, Filtering and Pagination

Task 3 extends the Employee Management API by adding search, filtering and pagination support to the `GET /employees` endpoint.

### Search by Employee Name

The `search` query parameter supports partial and case-insensitive employee name searches.

Example:

```text
GET /employees?search=john
```

This can also find names with different letter casing:

```text
GET /employees?search=JOHN
```

### Filter by Department

Employees can be filtered by department.

Example:

```text
GET /employees?department=IT
```

### Filter by Work Mode

Employees can be filtered by work mode.

Supported values:

* `WFH`
* `WFO`

Example:

```text
GET /employees?work_mode=WFH
```

### Filter by Active Status

Employees can be filtered using the `is_active` parameter.

Example:

```text
GET /employees?is_active=true
```

or:

```text
GET /employees?is_active=false
```

### Combined Filters

Multiple query parameters can be used together.

Example:

```text
GET /employees?search=john&department=IT&work_mode=WFH&is_active=true
```

The API applies all provided filters together.

### Pagination

Pagination is supported using `limit` and `offset`.

Example:

```text
GET /employees?limit=10&offset=0
```

* `limit` specifies the maximum number of employees to return.
* `offset` specifies the number of records to skip.

Example:

```text
GET /employees?limit=10&offset=10
```

This skips the first 10 records and returns the next set of records.

### Employee Listing Order

Employee records returned by `GET /employees` are ordered by employee ID in ascending order.

## API Examples

### Create Employee

```json
{
  "name": "John",
  "email": "john@example.com",
  "department": "IT",
  "primary_skill": "Python",
  "location": "Chennai",
  "work_mode": "WFH"
}
```

A successful request creates the employee in the MySQL database and returns the generated employee ID.

### Search Example

```text
GET /employees?search=john
```

Returns employees whose names partially match `john`, without considering letter case.

### Filter Example

```text
GET /employees?department=IT&work_mode=WFH
```

Returns employees who belong to the IT department and work from home.

### Pagination Example

```text
GET /employees?limit=5&offset=0
```

Returns the first 5 employees.

## Validation and Error Handling

The API validates incoming employee data and returns appropriate HTTP error responses.

Examples of handled cases include:

* Invalid email format
* Duplicate email address
* Duplicate email with different letter casing
* Invalid work mode
* Invalid employee ID
* Missing required fields
* Empty or whitespace-only required fields
* Employee not found
* Database errors

### Duplicate Email

Email addresses must be unique regardless of letter casing.

For example:

```text
john@example.com
JOHN@example.com
John@Example.com
```

These are treated as the same email address.

### Invalid Work Mode

Only the following values are accepted:

```text
WFH
WFO
```

An invalid value returns a validation error.

### Employee Not Found

If an employee ID does not exist, the API returns a `404 Not Found` response.

## Database Error Handling

Database operations use SQLAlchemy sessions.

If a database operation fails, the transaction is rolled back to prevent incomplete changes.

Database sessions are properly closed after use.

This prevents database connections from remaining open unnecessarily.

## Persistence Testing

Employee data is stored in MySQL, so the data remains available after restarting the FastAPI application.

Testing steps:

1. Start the FastAPI application.
2. Create an employee using Swagger UI.
3. Verify the employee using `GET /employees`.
4. Stop the FastAPI application.
5. Start the application again.
6. Call `GET /employees`.
7. Verify that the previously created employee is still available.

This confirms that employee data is persisted in the MySQL database instead of an in-memory Python list.

## Testing

The APIs were tested using Swagger UI.

The following scenarios were tested:

* Health check
* Create employee
* Get all employees
* Get employee by ID
* Update employee
* Delete employee
* Search by employee name
* Department filtering
* Work mode filtering
* Active/inactive filtering
* Combined filters
* Pagination using limit and offset
* Invalid email validation
* Invalid work mode validation
* Invalid employee ID validation
* Missing required fields
* Whitespace validation
* Duplicate email validation
* Case-insensitive duplicate email validation
* Employee not found
* Database persistence after application restart
* Database error handling

## Learning Notes

Through this project, I learned how to:

* Build REST APIs using FastAPI.
* Define request and response schemas using Pydantic.
* Connect FastAPI with MySQL.
* Use SQLAlchemy ORM for database operations.
* Create database models and tables.
* Manage SQLAlchemy database sessions.
* Implement CRUD operations using a database.
* Handle database transactions and rollbacks.
* Validate request data and query parameters.
* Implement case-insensitive email uniqueness.
* Implement search and filtering.
* Implement pagination using limit and offset.
* Preserve database-generated fields such as employee ID and `created_at`.
* Handle API and database errors properly.
* Test APIs using Swagger UI.
* Use Git and GitHub for version control.

## Task 3 Summary

Task 3 adds employee search, filtering and pagination capabilities while continuing to use the MySQL database and SQLAlchemy implementation from Task 2.

The existing CRUD APIs remain available, and the `GET /employees` endpoint now supports:

* Name search
* Department filtering
* Work mode filtering
* Active/inactive filtering
* Combined filters
* Pagination
* ID-based ordering
