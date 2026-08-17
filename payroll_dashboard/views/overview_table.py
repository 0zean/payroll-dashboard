import reflex as rx

from ..backend.schemas import Employee
from ..backend.table_state import TableState
from ..backend.utils import header_cell

CELL_STRONG_CLASS = "md-cell-primary"
CELL_CLASS = "md-cell"
CELL_NUMERIC_CLASS = "md-cell-numeric"
PAGER_BUTTON_CLASS = "md-press focus-ring"


def show_employee(user: Employee):
    """Show an employee in a table row."""
    return rx.table.row(
        rx.table.cell(user.employee_name, class_name=CELL_STRONG_CLASS),
        rx.table.cell(user.date, class_name=CELL_CLASS),
        rx.table.cell(user.hours_worked, class_name=CELL_NUMERIC_CLASS),
        align="center",
    )


def _pager_button(
    icon: str, event: rx.event.EventType, dimmed: rx.Var
) -> rx.Component:
    return rx.icon_button(
        rx.icon(icon, size=16),
        on_click=event,
        opacity=rx.cond(dimmed, 0.45, 1),
        color_scheme=rx.cond(dimmed, "gray", "accent"),
        variant="soft",
        radius="full",
        class_name=PAGER_BUTTON_CLASS,
        aria_label=icon,
    )


def _pagination_view() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "Page ",
            rx.el.span(
                TableState.page_number,
                class_name="tabular md-label-large md-on-surface",
            ),
            f" of {TableState.total_pages}",
            class_name="md-label-medium md-on-surface-variant",
        ),
        rx.el.div(
            _pager_button(
                "chevrons-left",
                TableState.first_page,  # type: ignore
                TableState.page_number == 1,
            ),
            _pager_button(
                "chevron-left",
                TableState.prev_page,  # type: ignore
                TableState.page_number == 1,
            ),
            _pager_button(
                "chevron-right",
                TableState.next_page,  # type: ignore
                TableState.page_number == TableState.total_pages,
            ),
            _pager_button(
                "chevrons-right",
                TableState.last_page,  # type: ignore
                TableState.page_number == TableState.total_pages,
            ),
            class_name="flex items-center gap-2",
        ),
        class_name=(
            "md-divider-top mt-4 flex w-full flex-col items-start gap-3 pt-4 "
            "sm:flex-row sm:items-center sm:justify-end sm:gap-5"
        ),
    )


def overview_table() -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        header_cell("Employee", "user"),
                        header_cell("Date", "calendar-days"),
                        header_cell("Hours", "clock"),
                    ),
                ),
                rx.table.body(
                    rx.foreach(TableState.get_current_page, show_employee)
                ),
                variant="surface",
                size="2",
                width="100%",
                on_mount=TableState.load_entries,  # type: ignore
                class_name="min-w-[520px]",
            ),
            class_name="data-table table-shell w-full overflow-x-auto",
        ),
        rx.cond(TableState.users, _pagination_view()),
    )
