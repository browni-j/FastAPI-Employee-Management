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
* Proper error handling
* Database transaction rollback on failed changes
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
Stackly_task/
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