import reflex as rx

from ..backend.schemas import Employee
from ..backend.table_state import TableState
from ..backend.utils import header_cell
from .table import _pagination_view


def show_employee(user: Employee):
    """Show an employee in a table row."""
    return rx.table.row(
        rx.table.cell(user.employee_name),
        rx.table.cell(user.date),
        rx.table.cell(user.hours_worked),
        align="center",
    )


def overview_table() -> rx.Component:
    return rx.fragment(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    header_cell("Employee", "user"),
                    header_cell("Date", "calendar-days"),
                    header_cell("Hours", "clock"),
                ),
            ),
            rx.table.body(rx.foreach(TableState.get_current_page, show_employee)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=TableState.load_entries,  # type: ignore
        ),
        rx.cond(TableState.users, _pagination_view()),
    )
