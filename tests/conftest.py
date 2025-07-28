from unittest.mock import MagicMock, patch

import pytest
import requests_mock as rm

from payroll_dashboard.backend.schemas import Employee
from payroll_dashboard.backend.table_state import TableState


@pytest.fixture(autouse=True)
def mock_supabase_env(monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("SUPABASE_URL", "http://mocked-url")
    monkeypatch.setenv("SUPABASE_KEY", "mocked-key")

    # Patch create_client before importing auth_state
    with patch("payroll_dashboard.backend.auth_state.create_client") as mock_create_client:
        mock_supabase = MagicMock()
        mock_create_client.return_value = mock_supabase
        yield mock_supabase  # yields to allow test code to run with the mock


@pytest.fixture
def requests_mock():
    with rm.Mocker() as m:
        yield m


@pytest.fixture
def sample_employee():
    return Employee(id=1, employee_name="Alice", hours_worked=8.0, date="01/01/2025", extra=1.0, notes="Good")


@pytest.fixture
def auth_state():
    from payroll_dashboard.backend.auth_state import AuthState

    return AuthState()


@pytest.fixture
def table_state():
    return TableState()
