from unittest.mock import patch

import pytest

from payroll_dashboard.backend.schemas import PayrollStats


def test_reset_form_fields(table_state):
    table_state.current_entry.employee_name = "Test"
    table_state.date_format = "2025-01-01"
    table_state.reset_form_fields()
    assert table_state.current_entry.employee_name == ""
    assert table_state.date_format == ""


def test_pagination_logic(table_state):
    table_state.total_items = 50
    table_state.limit = 10
    table_state.offset = 20
    assert table_state.page_number == 3
    # 50 items at 10 per page is exactly 5 pages; a 6th would be empty.
    assert table_state.total_pages == 5


@pytest.mark.parametrize(
    ("total_items", "expected_pages"),
    [(0, 1), (1, 1), (10, 1), (11, 2), (20, 2), (21, 3)],
)
def test_total_pages_boundaries(table_state, total_items, expected_pages):
    table_state.limit = 10
    table_state.total_items = total_items
    assert table_state.total_pages == expected_pages


def test_filter_and_sort(table_state, sample_employee):
    table_state.users = [
        sample_employee,
        sample_employee.model_copy(update={"employee_name": "Bob", "hours_worked": 4.0}),
        sample_employee.model_copy(update={"employee_name": "Zoe", "hours_worked": 6.0}),
    ]
    table_state.sort_value = "employee_name"
    table_state.sort_reverse = False
    sorted_users = table_state.filtered_sorted_items
    assert sorted_users[0].employee_name == "Alice"
    assert sorted_users[-1].employee_name == "Zoe"

    table_state.search_value = "zoe"
    filtered = table_state.filtered_sorted_items
    assert len(filtered) == 1
    assert filtered[0].employee_name == "Zoe"


def test_set_hours_worked_valid(table_state):
    table_state.set_hours_worked("4.5")
    assert table_state.current_entry.hours_worked == 4.5


def test_set_hours_worked_invalid(table_state):
    table_state.set_hours_worked("invalid")
    assert table_state.current_entry.hours_worked == 0.0


def test_set_date_valid_format(table_state):
    table_state.set_date("2025-01-01")
    assert table_state.current_entry.date == "01/01/2025"


@pytest.mark.asyncio
async def test_validation_errors_on_submit_add_employee(table_state):
    form_data = {"employee_name": "", "date": "", "hours_worked": "abc"}
    await table_state.submit_add_employee(form_data=form_data)
    assert table_state.show_validation_errors is True
    assert table_state.name_error
    assert table_state.date_error
    assert table_state.hours_error


def test_delete_entry_calls_reload(table_state, sample_employee):
    table_state.users = [sample_employee]
    with (
        patch("payroll_dashboard.backend.table_state.delete_employee"),
        patch("payroll_dashboard.backend.table_state.fetch_employees", return_value=[]),
        patch(
            "payroll_dashboard.backend.table_state.calculate_stats",
            return_value=PayrollStats(total_entries=0, total_hours=0, employees_count=0),
        ),
    ):
        table_state.delete_entry(sample_employee.id)
        assert table_state.users == []
        assert table_state.stats.total_entries == 0
