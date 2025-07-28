from unittest import mock

from payroll_dashboard.backend.schemas import Employee
from payroll_dashboard.backend.utils import calculate_stats, close_session_on_exit, header_cell


def test_close_session_on_exit_session_none(monkeypatch):
    # _session is None, should do nothing
    monkeypatch.setattr("payroll_dashboard.backend.utils._session", None)
    with mock.patch("payroll_dashboard.backend.utils.asyncio.run") as mock_run:
        close_session_on_exit()
        mock_run.assert_not_called()


def test_close_session_on_exit_session_closed(monkeypatch):
    # _session is set and closed
    fake_session = mock.Mock()
    fake_session.closed = True
    monkeypatch.setattr("payroll_dashboard.backend.utils._session", fake_session)
    with mock.patch("payroll_dashboard.backend.utils.asyncio.run") as mock_run:
        close_session_on_exit()
        mock_run.assert_not_called()


def test_close_session_on_exit_session_open(monkeypatch):
    # _session is set and not closed
    fake_session = mock.Mock()
    fake_session.closed = False
    monkeypatch.setattr("payroll_dashboard.backend.utils._session", fake_session)
    with mock.patch("payroll_dashboard.backend.utils.asyncio.run") as mock_run:
        close_session_on_exit()
        mock_run.assert_called_once()
        # Ensure it was called with _session.close()
        called_func = mock_run.call_args[0][0]
        # Should be a coroutine function
        assert callable(called_func)


def test_calculate_stats_empty():
    stats = calculate_stats([])
    assert stats.total_entries == 0
    assert stats.total_hours == 0
    assert stats.employees_count == 0


def test_calculate_stats_multiple():
    data = [
        Employee(id=1, employee_name="Alice", hours_worked=8, date="2024-06-01", extra=0, notes=""),
        Employee(id=2, employee_name="Bob", hours_worked=7.5, date="2024-06-01", extra=1, notes=""),
        Employee(id=3, employee_name="Alice", hours_worked=4, date="2024-06-02", extra=0, notes=""),
    ]
    stats = calculate_stats(data)
    assert stats.total_entries == 3
    assert stats.total_hours == 19.5
    assert stats.employees_count == 2


def test_header_cell_returns_component():
    # Just check it returns something (mock rx)
    with mock.patch("payroll_dashboard.backend.utils.rx") as rx_mock:
        header_cell("Test", "icon-name")
        assert rx_mock.table.column_header_cell.called
