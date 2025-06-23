import reflex as rx
from pydantic import BaseModel, Field


class Employee(BaseModel):
    """The employee model."""

    id: int = Field(description="Unique identifier for the employee")
    employee_name: str = Field(description="Full name of employee")
    hours_worked: float = Field(description="Number of hours worked on a given day")
    date: str = Field(description="Date employee worked")
    extra: float = Field(0.0, description="Extra hours worked")
    notes: str = Field("", description="Employee notes")


class EmployeeEntry(BaseModel):
    """The employee entry model."""
    
    employee_name: str
    hours_worked: float
    date: str
    extra_hours: float | None
    notes: str | None


class EmployeeWithPayRate (rx.Model, table=True):
    """The employee model with pay rate."""
    
    employee_name: str
    pay_rate: str


class PayrollStats(rx.Model, table=True):
    """The payroll statistics model."""
    
    totalEntries: int
    totalHours: int
    employeesCount: int