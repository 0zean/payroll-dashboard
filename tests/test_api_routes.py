import pytest
from aioresponses import aioresponses

from ..payroll_dashboard.backend.api_routes import (
    add_employee,
    clear_payroll,
    delete_employee,
    fetch_employee_names,
    fetch_employees,
    onboard_employee,
    sync_table,
    update_employee,
)
from ..payroll_dashboard.backend.schemas import EmployeeEntry, EmployeeOnboarding


def test_fetch_employee_names_success(requests_mock):
    mock_data = ["Alice", "Bob"]
    requests_mock.get("http://127.0.0.1:8000/api/employee-names", json=mock_data)
    result = fetch_employee_names()
    assert result == mock_data


def test_fetch_employees_success(requests_mock):
    mock_data = [{"name": "Alice", "id": 1}]
    requests_mock.get("http://127.0.0.1:8000/api/employees", json=mock_data)
    result = fetch_employees()
    assert result == mock_data


def test_delete_employee_success(requests_mock):
    requests_mock.delete("http://127.0.0.1:8000/api/employees", status_code=204)
    delete_employee(1)  # Should not raise


def test_add_employee_success(requests_mock):
    test_data = EmployeeEntry(
        employee_name="John Doe",
        hours_worked=5.0,
        date="07/11/2025",
        extra=0.0,
        notes="",
    )
    requests_mock.post("http://127.0.0.1:8000/api/employees", status_code=201)

    # Should not raise
    add_employee(test_data)


def test_update_employee_success(requests_mock):
    test_data = EmployeeEntry(
        employee_name="John Doe",
        hours_worked=5.0,
        date="07/11/2025",
        extra=0.0,
        notes="",
    )
    requests_mock.put("http://127.0.0.1:8000/api/employees", status_code=200)

    # Should not raise
    update_employee(123, test_data)


@pytest.mark.asyncio
async def test_clear_payroll_success():
    with aioresponses() as m:
        m.post("http://127.0.0.1:8000/api/clear-payroll", status=204)
        await clear_payroll()  # Should not raise


@pytest.mark.asyncio
async def test_sync_table_success():
    with aioresponses() as m:
        m.post("http://127.0.0.1:8000/api/sync", status=204)
        await sync_table()


@pytest.mark.asyncio
async def test_onboard_employee_success():
    employee = EmployeeOnboarding(employee_name="Test", pay_rate=20.0)
    with aioresponses() as m:
        m.post("http://127.0.0.1:8000/api/new-employee", status=201)
        await onboard_employee(employee)
