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
| `location`      |                            |
