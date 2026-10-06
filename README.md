# Employee Management API

A beginner-friendly FastAPI backend application for managing employees and work items using MySQL and SQLAlchemy.

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
* Work item management
* Employee and work item relationship using foreign key
* SQLAlchemy relationship between employees and work items
* Work item search by title
* Work item filtering by employee, status and priority
* Work item pagination
* Work item status and priority validation
* Work item title and description length validation
* Protection against deleting employees with assigned work items

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

### 2. Switch to the Task 4 Branch

```bash
git switch task-4
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

The application uses SQLAlchemy to create the required `employees` and `work_items` tables automatically when the application starts.

To verify the tables:

```sql
SHOW TABLES;
```

To view employee records:

```sql
SELECT * FROM employees;
```

To view work item records:

```sql
SELECT * FROM work_items;
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

| Method | Endpoint                     | Description                                                |
| ------ | ---------------------------- | ---------------------------------------------------------- |
| GET    | `/health`                    | Health check                                               |
| POST   | `/employees`                 | Create employee                                            |
| GET    | `/employees`                 | Get employees with optional search, filters and pagination |
| GET    | `/employees/{employee_id}`   | Get employee by ID                                         |
| PUT    | `/employees/{employee_id}`   | Update employee                                            |
| DELETE | `/employees/{employee_id}`   | Delete employee                                            |
| POST   | `/work-items`                | Create work item                                           |
| GET    | `/work-items`                | Get work items with search, filters and pagination         |
| GET    | `/work-items/{work_item_id}` | Get work item by ID                                        |
| PUT    | `/work-items/{work_item_id}` | Update work item                                           |
| DELETE | `/work-items/{work_item_id}` | Delete work item                                           |

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

## Task 4 - Work Item Management

Task 4 adds work item management and connects work items with employees using a foreign key and SQLAlchemy relationship.

### Work Item APIs

| Method | Endpoint                     | Description                                        |
| ------ | ---------------------------- | -------------------------------------------------- |
| POST   | `/work-items`                | Create work item                                   |
| GET    | `/work-items`                | Get work items with search, filters and pagination |
| GET    | `/work-items/{work_item_id}` | Get work item by ID                                |
| PUT    | `/work-items/{work_item_id}` | Update work item                                   |
| DELETE | `/work-items/{work_item_id}` | Delete work item                                   |

### Work Item Fields

| Field         | Description                                      |
| ------------- | ------------------------------------------------ |
| `id`          | Auto-generated work item ID                      |
| `title`       | Required work item title, maximum 255 characters |
| `description` | Optional description, maximum 1000 characters    |
| `employee_id` | Assigned employee ID                             |
| `status`      | `TODO`, `IN_PROGRESS`, or `COMPLETED`            |
| `priority`    | `LOW`, `MEDIUM`, or `HIGH`                       |
| `due_date`    | Optional due date                                |
| `created_at`  | Record creation timestamp                        |

### Employee Relationship

Each work item is assigned to an existing employee using the `employee_id` foreign key.

The SQLAlchemy relationship is defined between:

```text
Employee → WorkItem
```

One employee can have multiple work items, while each work item belongs to one employee.

The relationship allows the assigned employee details to be included in the work item response.

Example:

```json
{
  "id": 1,
  "title": "Prepare weekly status report",
  "employee_id": 2,
  "status": "TODO",
  "priority": "MEDIUM",
  "assigned_employee": {
    "id": 2,
    "name": "Employee Name",
    "email": "employee@example.com"
  }
}
```

### Search, Filters and Pagination

The `GET /work-items` endpoint supports:

* Title search using `search`
* Employee filtering using `employee_id`
* Status filtering using `status`
* Priority filtering using `priority`
* Pagination using `limit` and `offset`
* ID-based ascending order

Example:

```text
GET /work-items?employee_id=4&status=TODO&priority=MEDIUM&limit=10&offset=0
```

The `total` count is calculated before `limit` and `offset` are applied.

### Work Item Status

Supported status values:

```text
TODO
IN_PROGRESS
COMPLETED
```

An invalid status returns:

```text
422 Unprocessable Entity
```

### Work Item Priority

Supported priority values:

```text
LOW
MEDIUM
HIGH
```

An invalid priority returns:

```text
422 Unprocessable Entity
```

### Work Item Validation

The API validates:

* Employee existence
* Work item existence
* Positive employee ID
* Valid status values
* Valid priority values
* Required title
* Blank or whitespace-only title
* Maximum title length of 255 characters
* Maximum description length of 1000 characters

Invalid request data returns:

```text
422 Unprocessable Entity
```

Missing employees or work items return:

```text
404 Not Found
```

### Employee Deletion Protection

An employee cannot be deleted while work items are assigned to that employee.

If an employee has assigned work items, the API returns:

```text
400 Bad Request
```

with a message instructing the user to reassign or delete the assigned work items first.

This prevents foreign key relationship errors and protects related work item records.

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

### Create Work Item

```json
{
  "title": "Prepare weekly status report",
  "description": "Prepare and submit the weekly report",
  "employee_id": 2,
  "status": "TODO",
  "priority": "MEDIUM",
  "due_date": "2026-10-20"
}
```

The `employee_id` must belong to an existing employee.

### Search Work Items

```text
GET /work-items?search=report
```

Returns work items whose titles partially match the search value.

### Filter Work Items

```text
GET /work-items?employee_id=2&status=TODO&priority=HIGH
```

Returns work items matching all provided filters.

### Pagination Example

```text
GET /work-items?limit=5&offset=0
```

Returns the first 5 work items.

## Validation and Error Handling

The API validates incoming employee and work item data and returns appropriate HTTP error responses.

Examples of handled cases include:

* Invalid email format
* Duplicate email address
* Duplicate email with different letter casing
* Invalid work mode
* Invalid employee ID
* Missing required fields
* Empty or whitespace-only required fields
* Employee not found
* Work item not found
* Invalid work item status
* Invalid work item priority
* Work item title longer than 255 characters
* Work item description longer than 1000 characters
* Employee deletion while work items are assigned
* Database errors

## Database Error Handling

Database operations use SQLAlchemy sessions.

If a database operation fails, the transaction is rolled back to prevent incomplete changes.

Database sessions are properly closed after use.

This prevents database connections from remaining open unnecessarily.

## Persistence Testing

Employee and work item data are stored in MySQL, so the data remains available after restarting the FastAPI application.

Testing steps:

1. Start the FastAPI application.
2. Create an employee using Swagger UI.
3. Create a work item assigned to the employee.
4. Verify the employee and work item using the GET APIs.
5. Stop the FastAPI application.
6. Start the application again.
7. Call the GET APIs.
8. Verify that the previously created records are still available.

This confirms that data is persisted in the MySQL database instead of an in-memory Python list.

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
* Employee pagination
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
* Create work item
* Get work items
* Get work item by ID
* Update work item
* Delete work item
* Work item title search
* Work item employee filtering
* Work item status filtering
* Work item priority filtering
* Work item pagination
* Invalid work item status returns 422
* Invalid work item priority returns 422
* Invalid work item employee ID
* Work item not found
* Employee not found while creating/updating work item
* Blank work item title validation
* Work item title maximum length validation
* Work item description maximum length validation
* Employee deletion protection when work items are assigned
* Employee reassignment
* Work item persistence after application restart
* Existing employee API regression testing

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
* Create foreign key relationships between database tables.
* Define SQLAlchemy relationships.
* Assign work items to existing employees.
* Return related employee information in API responses.
* Preserve database-generated fields such as employee ID and `created_at`.
* Handle API and database errors properly.
* Test APIs using Swagger UI.
* Use Git and GitHub for version control.

## Task 3 Summary

Task 3 adds employee search, filtering and pagination capabilities while continuing to use the MySQL database and SQLAlchemy implementation from Task 2.

The existing CRUD APIs remain available, and the `GET /employees` endpoint supports:

* Name search
* Department filtering
* Work mode filtering
* Active/inactive filtering
* Combined filters
* Pagination
* ID-based ordering

## Task 4 Summary

Task 4 implements Work Item CRUD operations with employee assignment using a foreign key and SQLAlchemy relationship.

The `GET /work-items` endpoint supports:

* Title search
* Employee filtering
* Status filtering
* Priority filtering
* Pagination
* ID-based ordering

Task 4 also includes request validation, employee existence validation, work item existence validation, status and priority validation, title and description length validation, database persistence and protection against deleting employees who have assigned work items.

All existing employee APIs remain available and were regression tested to ensure that Task 4 changes do not break previous functionality.
