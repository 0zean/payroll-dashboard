import reflex as rx

from ..backend.table_state import Employee, TableState
from ..backend.utils import header_cell
from ..components.form_field import form_field
from ..components.icon import icon
from ..custom_components.reflex_react_select import react_select


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
                    icon("trash-2", size=20),
                    on_click=lambda: TableState.delete_entry(employee_id=user.id),  # type: ignore
                    size="2",
                    variant="ghost",
                    color_scheme="tomato",
                    aria_label="Delete entry",
                ),
                spacing="1",
            )
        ),
        align="center",
    )


def _dialog_header(icon_tag: str, title: str, description: str) -> rx.Component:
    """M3 dialog header: tonal icon container, headline-small title, body description."""
    return rx.hstack(
        rx.flex(
            icon(icon_tag, size=24, color="var(--md-sys-color-on-secondary-container)"),
            background="var(--md-sys-color-secondary-container)",
            border_radius="var(--md-sys-shape-corner-full)",
            min_width="3rem",
            height="3rem",
            align="center",
            justify="center",
        ),
        rx.vstack(
            rx.dialog.title(title, margin="0"),
            rx.dialog.description(description),
            spacing="1",
            align_items="start",
        ),
        spacing="4",
        margin_bottom="1.5em",
        align="center",
        width="100%",
    )


def _employee_form_fields(user: Employee | None = None) -> rx.Component:
    """The shared add/edit field set.

    Args:
        user: The employee being edited, or None when adding.

    Returns:
        The stacked form fields.

    """
    editing = user is not None
    return rx.flex(
        rx.vstack(
            rx.hstack(
                icon("user", size=18),
                rx.text("Employee", font="var(--md-sys-typescale-body-small)"),
                align="center",
                spacing="2",
            ),
            react_select(
                options=TableState.employee_dict,
                required=True,
                placeholder="Select Employee",
                width="100%",
                name="employee_name",
                is_clearable=True,
                is_searchable=True,
                **(
                    {
                        "input_id": "update_id",
                        "default_input_value": user.employee_name,
                        "class_name_prefix": "react-select-update",
                    }
                    if editing
                    else {"class_name_prefix": "react-select-add"}
                ),
            ),
            spacing="1",
            align_items="start",
            width="100%",
        ),
        form_field(
            "Date",
            "Date Worked",
            "date",
            "date",
            "calendar-days",
            TableState.date_format if editing else "",
            on=TableState.set_date,
            required=True,
            error_message=TableState.date_error,
        ),
        form_field(
            "Hours",
            "Hours worked",
            "number",
            "hours_worked",
            "clock",
            f"{user.hours_worked}" if editing else "",
            on=TableState.set_hours_worked,
            required=True,
            error_message=TableState.hours_error,
        ),
        form_field(
            "Extra Hours",
            "Extra hours worked",
            "number",
            "extra",
            "clock-arrow-up",
            f"{user.extra}" if editing else "",
            on=TableState.set_extra,
        ),
        form_field(
            "Notes",
            "Employee Notes",
            "text",
            "notes",
            "notebook-pen",
            user.notes if editing else "",
            on=TableState.set_notes,
        ),
        direction="column",
        spacing="3",
    )


def _dialog_actions(submit_label: str) -> rx.Component:
    """M3 dialog actions: text buttons, trailing aligned."""
    return rx.flex(
        rx.dialog.close(
            rx.button("Cancel", variant="ghost", color_scheme="gray"),
        ),
        rx.form.submit(
            rx.button(submit_label, variant="ghost"),
            as_child=True,
        ),
        padding_top="1.5em",
        spacing="2",
        justify="end",
    )


def add_employee_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                icon("plus", size=20),
                rx.text("Add Employee", display=["none", "none", "block"]),
                size="3",
                variant="solid",
            ),
        ),
        rx.dialog.content(
            _dialog_header("users", "Add New Employee", "Fill the form with the employee's info"),
            rx.form.root(
                _employee_form_fields(),
                _dialog_actions("Submit Employee"),
                on_submit=TableState.submit_add_employee,
                reset_on_submit=False,
            ),
            max_width="450px",
        ),
        open=TableState.dialog_open,
        on_open_change=lambda open: rx.cond(
            open,
            TableState.open_add_dialog(),
            TableState.close_add_dialog(),
        ),
    )


def update_employee_dialog(user: Employee):
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                icon("square-pen", size=20),
                size="2",
                variant="ghost",
                aria_label="Edit entry",
            ),
        ),
        rx.dialog.content(
            _dialog_header("square-pen", "Edit Employee", "Edit the Employee's info"),
            rx.form.root(
                _employee_form_fields(user),
                _dialog_actions("Update Employee"),
                on_submit=TableState.submit_update_employee,
                reset_on_submit=False,
                key=f"edit-form-{user.id}",
            ),
            max_width="450px",
            key=f"edit-dialog-{user.id}",
        ),
        open=TableState.edit_dialog_employee_id == user.id,
        on_open_change=lambda open: rx.cond(
            open,
            TableState.open_edit_dialog(user),
            TableState.close_edit_dialog(),
        ),
    )


def _page_button(icon_tag: str, on_click, disabled) -> rx.Component:
    return rx.icon_button(
        icon(icon_tag, size=20),
        on_click=on_click,
        disabled=disabled,
        variant="ghost",
        size="2",
    )


def _pagination_view() -> rx.Component:
    first = TableState.page_number == 1
    last = TableState.page_number == TableState.total_pages
    return rx.hstack(
        rx.text(
            f"Page {TableState.page_number} of {TableState.total_pages}",
            font="var(--md-sys-typescale-body-medium)",
            color="var(--md-sys-color-on-surface-variant)",
        ),
        rx.hstack(
            _page_button("chevrons-left", TableState.first_page, first),
            _page_button("chevron-left", TableState.prev_page, first),
            _page_button("chevron-right", TableState.next_page, last),
            _page_button("chevrons-right", TableState.last_page, last),
            align="center",
            spacing="1",
            justify="end",
        ),
        spacing="4",
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
            rx.icon_button(
                rx.cond(
                    TableState.sort_reverse,
                    icon("arrow-down-z-a", size=20),
                    icon("arrow-down-a-z", size=20),
                ),
                on_click=TableState.toggle_sort,  # type: ignore
                variant="ghost",
                size="3",
                aria_label="Toggle sort direction",
            ),
            rx.select(
                {"employee_name", "date", "hours_worked", "extra", "notes"},
                placeholder="Sort By: ...",
                size="3",
                on_change=lambda sort_value: TableState.sort_values(sort_value),  # type: ignore
            ),
            rx.input(
                rx.input.slot(icon("search", size=20)),
                placeholder="Search here...",
                size="3",
                max_width="225px",
                width="100%",
                variant="surface",
                on_change=lambda value: TableState.filter_values(value),  # type: ignore
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
                    header_cell("Employee", "user"),
                    header_cell("Date", "calendar-days"),
                    header_cell("Hours", "clock"),
                    header_cell("Extra Hours", "clock-arrow-up"),
                    header_cell("Notes", "notebook-pen"),
                    header_cell("Actions", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(TableState.get_current_page, show_employee)),
            variant="surface",
            size="3",
            width="100%",
            on_mount=TableState.load_entries,  # type: ignore
        ),
        _pagination_view(),
    )
