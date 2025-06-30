from datetime import datetime
from typing import List

import reflex as rx

from ..backend.api_routes import add_employee, delete_employee, fetch_employees, update_employee
from ..backend.schemas import Employee, EmployeeEntry


class TableState(rx.State):
    """The state class."""

    users: list[Employee] = []

    current_employee: Employee = Employee(id=0, employee_name="", hours_worked=0.0, date="", extra=0.0, notes="")

    current_entry: EmployeeEntry = EmployeeEntry(
        employee_name="",
        hours_worked=0.0,
        date="",
        extra=0.0,
        notes="",
    )

    date_format: str = ""
    edit_dialog_employee_id: int | None = None

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    show_validation_errors: bool = False
    name_error: str = ""
    date_error: str = ""
    hours_error: str = ""

    add_dialog_open: bool = False

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Employee]:
        items = self.users

        # Filter items based on selected item
        if self.sort_value:
            if self.sort_value in ["hours_worked", "extra"]:
                items = sorted(
                    items,
                    key=lambda item: float(getattr(item, self.sort_value)),
                    reverse=self.sort_reverse,
                )
            else:
                items = sorted(
                    items,
                    key=lambda item: str(getattr(item, self.sort_value)).lower(),
                    reverse=self.sort_reverse,
                )

        # Filter items based on search value
        if self.search_value:
            search_value = self.search_value.lower()
            items = [
                item
                for item in items
                if any(
                    search_value in str(getattr(item, attr)).lower()
                    for attr in [
                        "employee_name",
                        "notes",
                        "date",
                    ]
                )
            ]

        return items

    @rx.var(cache=True)
    def page_number(self) -> int:
        return (self.offset // self.limit) + 1

    @rx.var(cache=True)
    def total_pages(self) -> int:
        return (self.total_items // self.limit) + (1 if self.total_items % self.limit else 1)

    @rx.var(cache=True, initial_value=[])
    def get_current_page(self) -> list[Employee]:
        start_index = self.offset
        end_index = start_index + self.limit
        return self.filtered_sorted_items[start_index:end_index]

    def sort_values(self, sort_value: str):
        self.sort_value = sort_value
        self.load_entries()

    def filter_values(self, search_value):
        self.search_value = search_value
        self.load_entries()

    def get_user(self, user: Employee):
        self.date_format = datetime.strptime(user.date, "%m/%d/%Y").strftime("%Y-%m-%d")

        self.current_employee = user
        self.current_entry.employee_name = user.employee_name
        self.current_entry.hours_worked = user.hours_worked
        self.current_entry.date = user.date
        self.current_entry.extra = user.extra
        self.current_entry.notes = user.notes

    def reset_form_fields(self) -> None:
        """Reset all form fields to their default values."""
        self.current_entry = EmployeeEntry(
            employee_name="",
            hours_worked=0.0,
            date="",
            extra=0.0,
            notes="",
        )
        self.date_format = ""

    def _reset_validation_errors(self, dialog: bool = False):
        self.add_dialog_open = dialog
        self.show_validation_errors = False
        self.name_error = ""
        self.date_error = ""
        self.hours_error = ""

    def prev_page(self):
        if self.page_number > 1:
            self.offset -= self.limit

    def next_page(self):
        if self.page_number < self.total_pages:
            self.offset += self.limit

    def first_page(self):
        self.offset = 0

    def last_page(self):
        self.offset = (self.total_pages - 1) * self.limit

    def load_entries(self):
        entries = fetch_employees()
        if entries:
            self.users = [
                Employee(**entry)
                for entry in entries
                if isinstance(entry, dict) and all(isinstance(k, str) for k in entry.keys())
            ]
            self.total_items = len(self.users)
        else:
            self.users = []
            self.total_items = len(self.users)

    def toggle_sort(self):
        self.sort_reverse = not self.sort_reverse
        self.load_entries()

    def add_employee_entry(self, employee_entry: EmployeeEntry):
        add_employee(employee_entry=employee_entry)

    def update_employee_entry(self, employee_id: int, employee_entry: EmployeeEntry):
        update_employee(employee_id=employee_id, employee_entry=employee_entry)

    def delete_entry(self, employee_id: int):
        delete_employee(employee_id=employee_id)
        self.load_entries()

    @rx.event
    async def change_value(self, value: str):
        """Change the select value var."""
        self.current_entry.employee_name = value

    @rx.event
    def set_date(self, value: str):
        # Convert "yyyy-mm-dd" to "mm/dd/yyyy"
        try:
            formatted = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
            self.current_entry.date = formatted
        except Exception:
            self.current_entry.date = value

    @rx.event
    def set_hours_worked(self, value: str):
        try:
            self.current_entry.hours_worked = float(value) if value.strip() != "" else 0.0
        except (ValueError, TypeError):
            self.current_entry.hours_worked = 0.0

    @rx.event
    def set_extra(self, value: str):
        try:
            self.current_entry.extra = float(value) if value.strip() != "" else 0.0
        except (ValueError, TypeError):
            self.current_entry.extra = 0.0

    @rx.event
    def set_notes(self, value: str):
        self.current_entry.notes = value

    @rx.event
    async def submit_update_employee(self):
        """Gather current state and send update."""
        entry = self.current_entry.model_copy()

        if entry.extra is None:
            entry.extra = 0.0
        if entry.notes is None:
            entry.notes = ""

        self.update_employee_entry(self.current_employee.id, entry)
        self.load_entries()

    @rx.event
    async def submit_add_employee(self, form_data: dict):
        """Gather current state and send add."""
        self._reset_validation_errors(dialog=True)

        is_valid = True

        if not form_data.get("employee_name").strip():
            self.name_error = "Employee name is required"
            is_valid = False

        if not form_data.get("date").strip():
            self.date_error = "Date is required"
            is_valid = False

        try:
            hours_worked = float(form_data.get("hours_worked"))
            if hours_worked <= 0 or hours_worked % 0.5 != 0:
                self.hours_error = "Hours must be greater than 0 and a multiple of 0.5"
                is_valid = False
        except (ValueError, TypeError):
            self.hours_error = "Hours worked must be a valid number"
            is_valid = False

        if not is_valid:
            self.show_validation_errors = True
            return

        entry = self.current_entry.model_copy()
        if entry.extra is None:
            entry.extra = 0.0
        if entry.notes is None:
            entry.notes = ""

        self.add_employee_entry(entry)
        self.load_entries()
        self.reset_form_fields()
        self.add_dialog_open = False
        return rx.toast.success("Employee added successfully!", position="top-center")

    @rx.event
    def open_add_dialog(self):
        """Open the add employee dialog."""
        self._reset_validation_errors(dialog=True)

    @rx.event
    def close_add_dialog(self):
        """Close the add employee dialog."""
        self._reset_validation_errors(dialog=False)

    @rx.event
    def open_edit_dialog(self, user: Employee):
        self.get_user(user)
        self.edit_dialog_employee_id = user.id

    @rx.event
    def close_edit_dialog(self):
        self.edit_dialog_employee_id = None
