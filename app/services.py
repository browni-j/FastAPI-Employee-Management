employees = []

next_employee_id = 1


def create_employee(employee):
    global next_employee_id

    for existing_employee in employees:
        if existing_employee["email"].casefold() == employee.email.casefold():
            return None

    employee_data = employee.model_dump()

    employee_data["id"] = next_employee_id
    next_employee_id += 1

    employees.append(employee_data)

    return employee_data


def get_all_employees():
    return employees


def get_employee_by_id(employee_id):
    for employee in employees:
        if employee["id"] == employee_id:
            return employee

    return None


def update_employee(employee_id, employee):
    for existing_employee in employees:
        if existing_employee["id"] == employee_id:

            for other_employee in employees:
                if (
                    other_employee["id"] != employee_id
                    and other_employee["email"].casefold() == employee.email.casefold()
                ):
                    return "duplicate_email"

            created_at = existing_employee["created_at"]

            existing_employee.update(employee.model_dump())

            existing_employee["id"] = employee_id
            existing_employee["created_at"] = created_at

            return existing_employee

    return None


def delete_employee(employee_id):
    for index, employee in enumerate(employees):
        if employee["id"] == employee_id:
            deleted_employee = employees.pop(index)
            return deleted_employee

    return None