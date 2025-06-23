from typing import List
from datetime import datetime

import reflex as rx

from ..backend.schemas import Employee, EmployeeEntry
from ..backend.api_routes import delete_employee, fetch_employees, update_employee, add_employee


class TableState(rx.State):
    """The state class."""

    users: list[Employee] = []
    
    current_user: Employee = Employee(id=0, employee_name="", hours_worked=0.0, date="", extra=0.0, notes="")

    name: str = current_user.employee_name
    hours_worked: float = current_user.hours_worked
    date: str = current_user.date
    extra: float = current_user.extra
    notes: str = current_user.notes
    
    date_format: str = ""
    edit_dialog_employee_id: int | None = None

    search_value: str = ""
    sort_value: str = ""
    sort_reverse: bool = False

    total_items: int = 0
    offset: int = 0
    limit: int = 12  # Number of rows per page

    @rx.var(cache=True)
    def filtered_sorted_items(self) -> List[Employee]:
        items = self.users

        # Filter items based on selected item
        if self.sort_value:
            if self.sort_value in ["hours, extra_hours"]:
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
        return (self.total_items // self.limit) + (
            1 if self.total_items % self.limit else 1
        )

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
        
        self.current_user = user
        self.name = user.employee_name
        self.hours_worked = user.hours_worked
        self.date = user.date
        self.extra = user.extra
        self.notes = user.notes

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
            self.users = [Employee(**entry) for entry in entries if entry]
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
        update_employee(
            employee_id=employee_id,
            employee_entry=employee_entry
        )
    
    def delete_entry(self, employee_id: int):
        delete_employee(employee_id=employee_id)
        self.load_entries()
    
    @rx.event
    async def change_value(self, value: str):
        """Change the select value var."""
        self.name = value
        
    @rx.event
    def set_date(self, value: str):
        # Convert "yyyy-mm-dd" to "mm/dd/yyyy"
        try:
            formatted = datetime.strptime(value, "%Y-%m-%d").strftime("%m/%d/%Y")
            self.date = formatted
        except Exception:
            self.date = value

    @rx.event
    def set_hours_worked(self, value: str):
        self.hours_worked = float(value)

    @rx.event
    def set_extra(self, value: str):
        self.extra = float(value)

    @rx.event
    def set_notes(self, value: str):
        self.notes = value
        
    @rx.event
    async def submit_update_employee(self):
        """Gather current state and send update."""
        entry = EmployeeEntry(
            employee_name=self.name,
            hours_worked=self.hours_worked,
            date=self.date,
            extra_hours=self.extra,
            notes=self.notes,
        )
        self.update_employee_entry(self.current_user.id, entry)
        self.load_entries()
        
    @rx.event
    async def submit_add_employee(self):
        """Gather current state and send add."""
        entry = EmployeeEntry(
            employee_name=self.name,
            hours_worked=self.hours_worked,
            date=self.date,
            extra_hours=self.extra,
            notes=self.notes,
        )
        self.add_employee_entry(entry)
        self.load_entries()
        
    @rx.event
    def open_edit_dialog(self, user: Employee):
        self.get_user(user)
        self.edit_dialog_employee_id = user.id

    @rx.event
    def close_edit_dialog(self):
        self.edit_dialog_employee_id = None
