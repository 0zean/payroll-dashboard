import reflex as rx

from ..backend.schemas import Employee
from ..backend.table_state import TableState
from ..backend.utils import header_cell


def show_employee(user: Employee):
    """Show an employee in a table row."""
    return rx.table.row(
        rx.table.cell(user.employee_name),
        rx.table.cell(user.date),
        rx.table.cell(user.hours_worked),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def _pagination_view() -> rx.Component:
    return rx.hstack(
        rx.text(
            "Page ",
            rx.code(TableState.page_number),
            f" of {TableState.total_pages}",
            justify="end",
        ),
        rx.hstack(
            rx.icon_button(
                rx.icon("chevrons-left", size=18),
                on_click=TableState.first_page,  # type: ignore
                opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=18),
                on_click=TableState.prev_page,  # type: ignore
                opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=18),
                on_click=TableState.next_page,  # type: ignore
                opacity=rx.cond(TableState.page_number == TableState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    TableState.page_number == TableState.total_pages,
                    "gray",
                    "accent",
                ),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevrons-right", size=18),
                on_click=TableState.last_page,  # type: ignore
                opacity=rx.cond(TableState.page_number == TableState.total_pages, 0.6, 1),
                color_scheme=rx.cond(
                    TableState.page_number == TableState.total_pages,
                    "gray",
                    "accent",
                ),
                variant="soft",
            ),
            align="center",
            spacing="2",
            justify="end",
        ),
        spacing="5",
        margin_top="1em",
        align="center",
        width="100%",
        justify="end",
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
