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

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
```

### 3. Activate the Virtual Environment

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

### 4. Install Dependencies

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
| DELETE | `/employees/{employee_id}` | Delete an employee                                         |

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

## Employee Search, Filtering and Pagination

The `GET /employees` endpoint supports optional query parameters for searching, filtering, and pagination.

| Query Parameter | Description                                    | Default | Validation        |
| --------------- | ---------------------------------------------- | ------- | ----------------- |
| `search`        | Partial employee name search, case-insensitive | None    | Optional          |
| `department`    | Filter employees by department                 | None    | Optional          |
| `work_mode`     | Filter employees by work mode                  | None    | `WFH` or `WFO`    |
| `is_active`     | Filter employees by active status              | None    | `true` or `false` |
| `limit`         | Maximum number of records to return            | `10`    | `1-100`           |
| `offset`        | Number of records to skip                      | `0`     | `0` or greater    |

### Search by Employee Name

The `search` parameter supports partial and case-insensitive employee name searches.

Example:

```text
GET /employees?search=brow
```

### Filter by Department

The `department` parameter filters employees by department.

Example:

```text
GET /employees?department=IT
```

### Filter by Work Mode

The `work_mode` parameter supports:

* `WFH`
* `WFO`

Example:

```text
GET /employees?work_mode=WFH
```

### Filter by Active Status

The `is_active` parameter can be used to filter active or inactive employees.

Example:

```text
GET /employees?is_active=true
```

For inactive employees:

```text
GET /employees?is_active=false
```

### Combined Filters

Multiple filters can be used together.

Example:

```text
GET /employees?department=IT&work_mode=WFO&is_active=true
```

### Pagination

The `limit` parameter controls the maximum number of records returned, while `offset` specifies the number of records to skip.

Example:

```text
GET /employees?limit=10&offset=0
```

Another page:

```text
GET /employees?limit=10&offset=10
```

### Search with Pagination

Search and pagination can also be combined.

Example:

```text
GET /employees?search=brow&limit=5&offset=0
```

### Response Format

The `/employees` endpoint returns the total number of matching records before pagination, along with the requested limit, offset, and employee records.

Example:

```json
{
  "total": 2,
  "limit": 10,
  "offset": 0,
  "items": [
    {
      "name": "Employee Name",
      "email": "employee@example.com",
      "department": "IT",
      "primary_skill": "Python",
      "location": "Nagercoil",
      "work_mode": "WFO",
      "is_active": true,
      "id": 1,
      "created_at": "2026-09-17T10:58:12"
    }
  ]
}
```

Employees are returned in ascending order by employee ID.

If no employees match the specified filters, the API returns HTTP `200` with `total` as `0` and an empty `items` array.

Example:

```json
{
  "total": 0,
  "limit": 10,
  "offset": 0,
  "items": []
}
```

If the offset is greater than the number of matching records, the API returns an empty `items` array while maintaining the correct `total`.

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
* Invalid pagination limits
* Invalid pagination offsets

Pagination validation:

* `limit` must be between `1` and `100`.
* `offset` must be `0` or greater.
* `work_mode` must be either `WFH` or `WFO`.

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

## Task 3 Testing Evidence

The `screenshots` folder contains API testing evidence for search, filtering, pagination, validation, and existing CRUD functionality.

The following scenarios were tested through Swagger UI:

* Employee name search
* Case-insensitive partial name search
* Department filtering
* Work mode filtering
* Active employee filtering
* Inactive employee filtering
* Combined filters
* Pagination using `limit` and `offset`
* Multiple pagination pages
* No-match search results
* Offset beyond available records
* Invalid work mode validation
* Invalid `limit` validation
* Invalid `offset` validation
* GET employee by ID regression test
* PUT employee update regression test
* DELETE employee regression test
* POST employee creation regression test

All tested scenarios returned the expected API responses.

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
* Implement SQLAlchemy query-based filtering.
* Implement case-insensitive partial name searches using `ilike`.
* Combine multiple optional query filters.
* Implement pagination using `limit` and `offset`.
* Calculate total matching records before pagination.
* Validate query parameters using FastAPI `Query`.

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

### Search and Filtering

The employee listing endpoint was extended to support optional search and filter parameters. SQLAlchemy query filters are applied directly to the database query instead of filtering records in Python.

### Pagination

Pagination was implemented using SQLAlchemy `offset()` and `limit()` methods. The total number of matching records is calculated before pagination so that clients can understand the available result count.

### Query Parameter Validation

FastAPI `Query` validation was used to ensure that `limit` remains between `1` and `100`, `offset` is non-negative, and `work_mode` accepts only `WFH` or `WFO`.

## Conclusion

Task 3 extends the Employee Management API with employee search, filtering, and pagination capabilities. The API supports case-insensitive name search, department filtering, work mode filtering, active status filtering, combined filters, and pagination using limit and offset.

All filtering and pagination operations are performed at the SQLAlchemy query level while maintaining the existing MySQL database-backed CRUD functionality. Existing create, read, update, and delete APIs were also regression tested to ensure that the Task 3 changes did not affect the existing functionality.
