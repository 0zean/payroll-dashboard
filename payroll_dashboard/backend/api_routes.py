import aiohttp
import requests

from ..backend.schemas import Employee, EmployeeEntry, EmployeeOnboarding

url_base = "http://127.0.0.1:8000/api/"


def fetch_employee_names() -> list[str | None]:
    """
    Fetches employee names from the API.

    Returns:
        list: A list of employee names or an empty list if the request fails.
    """
    try:
        response = requests.get(f"{url_base}employee-names")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching employee names: {e}")
        return []


def fetch_employees() -> list[Employee | None]:
    """
    Fetches employee data from the API.

    Returns:
        list: A list of employee data dictionaries or an empty list if the request fails.
    """
    try:
        response = requests.get(f"{url_base}employees")
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching employees: {e}")
        return []


def delete_employee(employee_id: int) -> None:
    """
    Deletes an employee by ID.

    Args:
        employee_id (int): The ID of the employee to delete.
    """
    try:
        response = requests.delete(f"{url_base}employees", params={"employee_id": employee_id})
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error deleting employee with ID {employee_id}: {e}")
        raise e


def update_employee(employee_id: int, employee_entry: EmployeeEntry) -> None:
    """
    Updates an employee's data by ID.

    Args:
        employee_id (int): The ID of the employee to update.
        employee_entry (EmployeeEntry): Updated employee info.
    """
    try:
        response = requests.put(
            f"{url_base}employees", params={"employee_id": employee_id}, json=employee_entry.model_dump()
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error updating employee with ID {employee_id}: {e}")
        raise e


def add_employee(employee_entry: EmployeeEntry) -> None:
    """
    Adds a new employee entry to the database.

    Args:
        employee_entry (EmployeeEntry): The employee entry to add.
    """
    try:
        response = requests.post(f"{url_base}employees", json=employee_entry.model_dump())
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error adding employee: {e}")
        raise e


async def onboard_employee(new_employee: EmployeeOnboarding) -> None:
    """
    Onboard a new employee into the Master List asynchronously

    Args:
        new_employee (EmployeeOnboarding): The new employee's info.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{url_base}new-employee", json=new_employee.model_dump()) as response:
                response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error adding new employee: {e}")
        raise e


async def sync_table() -> None:
    try:
        async with aiohttp.ClientSession() as session:
            await session.post(f"{url_base}sync")
    except requests.RequestException as e:
        print(f"Error syncing employees to Sheets: {e}")
        raise e
