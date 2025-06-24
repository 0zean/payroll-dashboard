import reflex as rx

from ..backend.api_routes import fetch_employee_names
from ..backend.table_state import Employee, TableState
from ..components.form_field import form_field


def show_employee(user: Employee):
    """Show an employee in a table row."""
    return rx.table.row(
        rx.table.cell(user.employee_name),
        rx.table.cell(user.date),
        rx.table.cell(user.hours_worked),
        rx.table.cell(rx.cond(user.extra == 0, "-", user.extra)),
        rx.table.cell(rx.cond(user.notes == "", "-", user.notes)),
        rx.table.cell(
            rx.hstack(
                update_employee_dialog(user),
                rx.icon_button(
                    rx.icon("trash-2", size=22),
                    on_click=lambda: TableState.delete_entry(employee_id=user.id),
                    size="2",
                    variant="solid",
                    color_scheme="red",
                ),
            )
        ),
        style={"_hover": {"bg": rx.color("gray", 3)}},
        align="center",
    )


def add_employee_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=26),
                rx.text("Add Employee", size="4", display=["none", "none", "block"]),
                size="3",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="users", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Customer",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Fill the form with the customer's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        rx.vstack(
                            rx.hstack(
                                rx.icon("user", size=16, stroke_width=1.5),
                                rx.text("Employee"),
                                align="center",
                                spacing="2",
                            ),
                            rx.select(
                                fetch_employee_names(),
                                on_change=TableState.change_value,
                                required=True,
                                placeholder="Select Employee",
                                width="100%",
                            ),
                        ),
                        # Date
                        form_field("Date", "Date Worked", "date", "date", "calendar-days", on=TableState.set_date),
                        # Hours
                        form_field(
                            "Hours", "Hours worked", "number", "hours_worked", "clock", on=TableState.set_hours_worked
                        ),
                        # Extra Hours
                        form_field(
                            "Extra Hours",
                            "Extra hours worked",
                            "number",
                            "extra",
                            "clock-arrow-up",
                            on=TableState.set_extra,
                        ),
                        # Notes
                        form_field(
                            "Notes",
                            "Employee Notes",
                            "text",
                            "notes",
                            "notebook-pen",
                            on=TableState.set_notes,
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Submit Customer"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=TableState.submit_add_employee,
                    reset_on_submit=False,
                ),
                width="100%",
                direction="column",
                spacing="4",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
        ),
    )


def update_employee_dialog(user):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("square-pen", size=22),
                rx.text("Edit", size="3"),
                color_scheme="blue",
                size="2",
                variant="solid",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=34),
                    color_scheme="grass",
                    radius="full",
                    padding="0.65rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Edit Employee",
                        weight="bold",
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Edit the Employee's info",
                    ),
                    spacing="1",
                    height="100%",
                    align_items="start",
                ),
                height="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
                width="100%",
            ),
            rx.flex(
                rx.form.root(
                    rx.flex(
                        # Name
                        rx.vstack(
                            rx.hstack(
                                rx.icon("user", size=16, stroke_width=1.5),
                                rx.text("Employee"),
                                align="center",
                                spacing="2",
                            ),
                            rx.select(
                                fetch_employee_names(),
                                default_value=user.employee_name,
                                on_change=TableState.change_value,
                                required=True,
                                placeholder="Select Employee",
                                width="100%",
                            ),
                        ),
                        # Date
                        form_field(
                            "Date",
                            "Date Worked",
                            "date",
                            "date",
                            "calendar-days",
                            TableState.date_format,
                            on=TableState.set_date,
                        ),
                        # Hours
                        form_field(
                            "Hours",
                            "Enter Hours Worked",
                            "number",
                            "hours_worked",
                            "clock",
                            user.hours_worked.to(str),
                            on=TableState.set_hours_worked,
                        ),
                        # Extra Hours
                        form_field(
                            "Extra Hours",
                            "Extra hours worked",
                            "number",
                            "extra",
                            "clock-arrow-up",
                            user.extra.to(str),
                            on=TableState.set_extra,
                        ),
                        # Notes
                        form_field(
                            "Notes",
                            "Employee Notes",
                            "text",
                            "notes",
                            "notebook-pen",
                            user.notes,
                            on=TableState.set_notes,
                        ),
                        direction="column",
                        spacing="3",
                    ),
                    rx.flex(
                        rx.dialog.close(
                            rx.button(
                                "Cancel",
                                variant="soft",
                                color_scheme="gray",
                            ),
                        ),
                        rx.form.submit(
                            rx.dialog.close(
                                rx.button("Update Employee"),
                            ),
                            as_child=True,
                        ),
                        padding_top="2em",
                        spacing="3",
                        mt="4",
                        justify="end",
                    ),
                    on_submit=TableState.submit_update_employee,
                    reset_on_submit=False,
                    key=f"edit-form-{user.id}",
                ),
                width="100%",
                direction="column",
                spacing="4",
                key=f"edit-form-{user.id}",
            ),
            max_width="450px",
            padding="1.5em",
            border=f"2px solid {rx.color('accent', 7)}",
            border_radius="25px",
            key=f"edit-dialog-{user.id}",
        ),
        open=TableState.edit_dialog_employee_id == user.id,
        on_open_change=lambda open: rx.cond(
            open,
            TableState.open_edit_dialog(user),
            TableState.close_edit_dialog(),
        ),
    )


def _header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
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
                on_click=TableState.first_page,
                opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-left", size=18),
                on_click=TableState.prev_page,
                opacity=rx.cond(TableState.page_number == 1, 0.6, 1),
                color_scheme=rx.cond(TableState.page_number == 1, "gray", "accent"),
                variant="soft",
            ),
            rx.icon_button(
                rx.icon("chevron-right", size=18),
                on_click=TableState.next_page,
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
                on_click=TableState.last_page,
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


def main_table() -> rx.Component:
    return rx.fragment(
        rx.flex(
            add_employee_button(),
            rx.spacer(),
            rx.cond(
                TableState.sort_reverse,
                rx.icon(
                    "arrow-down-z-a",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=TableState.toggle_sort,
                ),
                rx.icon(
                    "arrow-down-a-z",
                    size=28,
                    stroke_width=1.5,
                    cursor="pointer",
                    on_click=TableState.toggle_sort,
                ),
            ),
            rx.select(
                {"employee_name", "date", "hours_worked", "extra", "notes"},
                placeholder="Sort By: ...",
                size="3",
                on_change=lambda sort_value: TableState.sort_values(sort_value),
            ),
            rx.input(
                rx.input.slot(rx.icon("search")),
                placeholder="Search here...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=lambda value: TableState.filter_values(value),
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
            padding_bottom="1em",
        ),
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    _header_cell("Employee", "user"),
                    _header_cell("Date", "calendar-days"),
                    _header_cell("Hours", "clock"),
                    _header_cell("Extra Hours", "clock-arrow-up"),
                    _header_cell("Notes", "notebook-pen"),
                    _header_cell("Actions", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(TableState.get_current_page, show_employee)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=TableState.load_entries,
        ),
        _pagination_view(),
    )
