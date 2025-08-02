from unittest.mock import patch

import httpx
import pytest
from aioresponses import aioresponses

from payroll_dashboard.backend.api_routes import (
    add_employee,
    clear_payroll,
    delete_employee,
    fetch_employee_names,
    fetch_employees,
    onboard_employee,
    sync_table,
    update_employee,
)
from payroll_dashboard.backend.schemas import EmployeeEntry, EmployeeOnboarding
from tests.mock_utils import make_mock_handler


def test_fetch_employee_names_success(mock_httpx_client):
    mock_data = ["Alice", "Bob"]

    handler = make_mock_handler(
        expected_method="GET",
        expected_url="http://127.0.0.1:8000/api/employee-names",
        response_data=mock_data,
    )
    mock_client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.api_routes.get_client", return_value=mock_client):
        result = fetch_employee_names()
        assert result == mock_data


def test_fetch_employees_success(mock_httpx_client):
    mock_data = [{"name": "Alice", "id": 1}]

    handler = make_mock_handler(
        expected_method="GET",
        expected_url="http://127.0.0.1:8000/api/employees",
        response_data=mock_data,
    )
    mock_client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.api_routes.get_client", return_value=mock_client):
        result = fetch_employees()
        assert result == mock_data


def test_delete_employee_success(mock_httpx_client):
    handler = make_mock_handler(
        expected_method="DELETE",
        expected_url="http://127.0.0.1:8000/api/employees?employee_id=1",
        response_data=None,
        status_code=httpx.codes.NO_CONTENT,
    )
    mock_client = mock_httpx_client(handler)
    with patch("payroll_dashboard.backend.api_routes.get_client", return_value=mock_client):
        delete_employee(1)  # Should not raise


def test_add_employee_success(mock_httpx_client):
    test_data = EmployeeEntry(
        employee_name="John Doe",
        hours_worked=5.0,
        date="07/11/2025",
        extra=0.0,
        notes="",
    )
    handler = make_mock_handler(
        expected_method="POST",
        expected_url="http://127.0.0.1:8000/api/employees",
        response_data=None,
        status_code=httpx.codes.CREATED,
        expected_json=test_data.model_dump(),
    )
    mock_client = mock_httpx_client(handler)
    with patch("payroll_dashboard.backend.api_routes.get_client", return_value=mock_client):
        add_employee(test_data)  # Should not raise


def test_update_employee_success(mock_httpx_client):
    test_data = EmployeeEntry(
        employee_name="John Doe",
        hours_worked=5.0,
        date="07/11/2025",
        extra=0.0,
        notes="",
    )
    handler = make_mock_handler(
        expected_method="PUT",
        expected_url="http://127.0.0.1:8000/api/employees?employee_id=123",
        response_data=None,
        expected_json=test_data.model_dump(),
    )
    mock_client = mock_httpx_client(handler)
    with patch("payroll_dashboard.backend.api_routes.get_client", return_value=mock_client):
        update_employee(123, test_data)  # Should not raise


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
