import reflex as rx

from ..backend.schemas import Employee, PayrollStats


def calculate_stats(data: list[Employee]) -> PayrollStats:
    total_hours = sum(employee.hours_worked for employee in data)
    unique_employees = len(set(employee.employee_name for employee in data))

    return PayrollStats(total_entries=len(data), total_hours=total_hours, employees_count=unique_employees)


def header_cell(text: str, icon: str) -> rx.Component:
    return rx.table.column_header_cell(
        rx.hstack(
            rx.icon(icon, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )
