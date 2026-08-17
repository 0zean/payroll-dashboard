import reflex as rx

from .. import styles
from ..backend.table_state import Employee, TableState
from ..backend.utils import header_cell
from ..components.form_field import form_field
from ..custom_components.reflex_react_select import react_select

CELL_STRONG_CLASS = "text-[13px] font-semibold text-white"
CELL_CLASS = "text-[13px] font-medium text-white/70"
CELL_NUMERIC_CLASS = "tabular text-[13px] font-medium text-white/70"
MUTED_CLASS = "text-[13px] font-medium text-white/35"
TACTILE_CLASS = "press focus-ring"
DIALOG_CLASS = "glass-card rounded-2xl"
FIELD_LABEL_CLASS = (
    "text-[11px] font-semibold uppercase tracking-[0.14em] text-white/55"
)


def show_employee(user: Employee):
    """Show an employee in a table row."""
    return rx.table.row(
        rx.table.cell(user.employee_name, class_name=CELL_STRONG_CLASS),
        rx.table.cell(user.date, class_name=CELL_CLASS),
        rx.table.cell(user.hours_worked, class_name=CELL_NUMERIC_CLASS),
        rx.table.cell(
            rx.cond(
                user.extra == 0,
                rx.el.span("-", class_name=MUTED_CLASS),
                rx.el.span(user.extra, class_name=CELL_NUMERIC_CLASS),
            ),
        ),
        rx.table.cell(
            rx.cond(
                user.notes == "",
                rx.el.span("-", class_name=MUTED_CLASS),
                rx.el.span(user.notes, class_name=CELL_CLASS),
            ),
        ),
        rx.table.cell(
            rx.el.div(
                update_employee_dialog(user),
                rx.icon_button(
                    rx.icon("trash-2", size=17),
                    on_click=lambda: TableState.delete_entry(
                        employee_id=user.id
                    ),  # type: ignore
                    size="2",
                    variant="surface",
                    color_scheme="tomato",
                    radius="large",
                    class_name=TACTILE_CLASS,
                ),
                class_name="flex items-center justify-start gap-2",
            ),
        ),
        align="center",
    )


def add_employee_button() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=18),
                rx.text(
                    "Add Employee",
                    size="3",
                    display=["none", "none", "block"],
                ),
                size="3",
                variant="surface",
                class_name=f"{TACTILE_CLASS} font-semibold",
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="users", size=22),
                    color_scheme="grass",
                    variant="soft",
                    radius="full",
                    padding="0.6rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Add New Employee",
                        weight="bold",
                        margin="0",
                        class_name="tracking-tight text-white",
                    ),
                    rx.dialog.description(
                        "Fill the form with the employee's info",
                        class_name="text-[13px] text-white/55",
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
                                rx.icon("user", size=15, stroke_width=1.5),
                                rx.el.span(
                                    "Employee", class_name=FIELD_LABEL_CLASS
                                ),
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
                                class_name_prefix="react-select-add",
                            ),
                        ),
                        # Date
                        form_field(
                            "Date",
                            "Date Worked",
                            "date",
                            "date",
                            "calendar-days",
                            on=TableState.set_date,
                            required=True,
                            error_message=TableState.date_error,
                        ),
                        # Hours
                        form_field(
                            "Hours",
                            "Hours worked",
                            "number",
                            "hours_worked",
                            "clock",
                            on=TableState.set_hours_worked,
                            required=True,
                            error_message=TableState.hours_error,
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
                                class_name=TACTILE_CLASS,
                            ),
                        ),
                        rx.form.submit(
                            rx.button(
                                "Submit Employee",
                                class_name=f"{TACTILE_CLASS} font-semibold",
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
            class_name=DIALOG_CLASS,
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
                rx.icon("square-pen", size=17),
                color_scheme="blue",
                size="2",
                variant="surface",
                radius="large",
                class_name=TACTILE_CLASS,
            ),
        ),
        rx.dialog.content(
            rx.hstack(
                rx.badge(
                    rx.icon(tag="square-pen", size=22),
                    color_scheme="grass",
                    variant="soft",
                    radius="full",
                    padding="0.6rem",
                ),
                rx.vstack(
                    rx.dialog.title(
                        "Edit Employee",
                        weight="bold",
                        margin="0",
                        class_name="tracking-tight text-white",
                    ),
                    rx.dialog.description(
                        "Edit the Employee's info",
                        class_name="text-[13px] text-white/55",
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
                                rx.icon("user", size=15, stroke_width=1.5),
                                rx.el.span(
                                    "Employee", class_name=FIELD_LABEL_CLASS
                                ),
                                align="center",
                                spacing="2",
                            ),
                            react_select(
                                input_id="update_id",
                                options=TableState.employee_dict,
                                required=True,
                                default_input_value=user.employee_name,
                                placeholder="Select Employee",
                                width="100%",
                                name="employee_name",
                                is_clearable=True,
                                is_searchable=True,
                                class_name_prefix="react-select-update",
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
                            required=True,
                            error_message=TableState.date_error,
                        ),
                        # Hours
                        form_field(
                            "Hours",
                            "Enter Hours Worked",
                            "number",
                            "hours_worked",
                            "clock",
                            f"{user.hours_worked}",
                            on=TableState.set_hours_worked,
                            required=True,
                            error_message=TableState.hours_error,
                        ),
                        # Extra Hours
                        form_field(
                            "Extra Hours",
                            "Extra hours worked",
                            "number",
                            "extra",
                            "clock-arrow-up",
                            f"{user.extra}",
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
                                class_name=TACTILE_CLASS,
                            ),
                        ),
                        rx.form.submit(
                            rx.button(
                                "Update Employee",
                                class_name=f"{TACTILE_CLASS} font-semibold",
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
            class_name=DIALOG_CLASS,
            key=f"edit-dialog-{user.id}",
        ),
        open=TableState.edit_dialog_employee_id == user.id,
        on_open_change=lambda open: rx.cond(
            open,
            TableState.open_edit_dialog(user),
            TableState.close_edit_dialog(),
        ),
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
        radius="large",
        class_name=TACTILE_CLASS,
    )


def _pagination_view() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "Page ",
            rx.el.span(
                TableState.page_number,
                class_name="tabular font-semibold text-white",
            ),
            f" of {TableState.total_pages}",
            class_name="text-xs font-medium text-white/50",
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
            "flex w-full flex-col items-start gap-3 sm:flex-row sm:items-center "
            "sm:justify-end sm:gap-5"
        ),
    )


def _sort_toggle() -> rx.Component:
    return rx.el.button(
        rx.cond(
            TableState.sort_reverse,
            rx.icon("arrow-down-z-a", size=17, stroke_width=1.5),
            rx.icon("arrow-down-a-z", size=17, stroke_width=1.5),
        ),
        on_click=TableState.toggle_sort,  # type: ignore
        aria_label="Toggle sort direction",
        class_name=(
            "press focus-ring flex h-10 w-10 shrink-0 items-center justify-center "
            "rounded-xl border border-white/10 bg-white/5 text-white/70 "
            "transition-colors duration-200 hover:border-white/20 hover:bg-white/10 hover:text-white"
        ),
    )


def table_toolbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            add_employee_button(),
            class_name="flex shrink-0 items-center",
        ),
        rx.el.div(
            _sort_toggle(),
            rx.select(
                {"employee_name", "date", "hours_worked", "extra", "notes"},
                placeholder="Sort By: ...",
                size="3",
                radius="large",
                on_change=lambda sort_value: TableState.sort_values(sort_value),  # type: ignore
                class_name="min-w-[10rem] flex-1 sm:flex-none",
            ),
            rx.input(
                rx.input.slot(rx.icon("search", size=16), padding_left="0"),
                placeholder="Search here...",
                size="3",
                width="100%",
                radius="large",
                style=styles.ghost_input_style,
                on_change=lambda value: TableState.filter_values(value),  # type: ignore
                class_name="w-full sm:max-w-[240px]",
            ),
            class_name=(
                "flex w-full flex-col gap-3 sm:flex-row sm:flex-wrap sm:items-center "
                "sm:justify-end"
            ),
        ),
        class_name=(
            "glass-card spotlight control-bar flex w-full flex-col gap-3 p-3 "
            "sm:flex-row sm:items-center sm:justify-between"
        ),
    )


def main_table() -> rx.Component:
    return rx.el.div(
        table_toolbar(),
        rx.el.div(
            rx.el.div(
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
                    rx.table.body(
                        rx.foreach(TableState.get_current_page, show_employee)
                    ),
                    variant="surface",
                    size="2",
                    width="100%",
                    on_mount=TableState.load_entries,  # type: ignore
                    class_name="min-w-[880px]",
                ),
                class_name="data-table table-shell w-full overflow-x-auto",
            ),
            rx.el.div(
                _pagination_view(),
                class_name="w-full border-t border-white/8 px-3 py-3 sm:px-4",
            ),
            class_name="glass-card spotlight w-full overflow-hidden rounded-2xl",
        ),
        class_name="flex w-full flex-col gap-4",
    )
