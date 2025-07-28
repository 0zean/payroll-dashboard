import pytest
import requests_mock as rm

from payroll_dashboard.backend.auth_state import AuthState
from payroll_dashboard.backend.schemas import Employee
from payroll_dashboard.backend.table_state import TableState


@pytest.fixture
def requests_mock():
    with rm.Mocker() as m:
        yield m


@pytest.fixture
def sample_employee():
    return Employee(id=1, employee_name="Alice", hours_worked=8.0, date="01/01/2025", extra=1.0, notes="Good")


@pytest.fixture
def auth_state():
    return AuthState()


@pytest.fixture
def table_state():
    return TableState()
