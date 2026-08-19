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
    extra: float
    notes: str


class EmployeeOnboarding(BaseModel):
    """The employee onboarding model with pay rate."""

    employee_name: str
    pay_rate: float


class PayrollStats(BaseModel):
    """The payroll statistics model."""

    total_entries: float
    total_hours: float
    employees_count: float


class EventEntry(BaseModel):
    """The editable half of an event row.

    Mirrors the API's EventEntry: the ``*_sent`` flags are owned by the ecas
    service and are never written from the dashboard.
    """

    event_id: str
    event_name: str
    start_date: str = Field(description="ISO date, e.g. 2026-05-01")
    end_date: str = Field(description="ISO date, e.g. 2026-05-03")
    start_time: str = ""
    end_time: str = ""
    location_name: str = ""
    location_address: str = ""
    recipients: list[str] = Field(default_factory=list)
    platform: str = "direct"
    contact_phone: str = ""
    contact_email: str = ""
    event_details: str = Field("", description="Free-form context for LLM email generation")


class EmailSchedule(BaseModel):
    """What ecas will do with one email type, derived by the API."""

    email_type: str
    trigger_date: str | None = None
    status: str = Field(description="sent, due, scheduled, missed or inactive")
    sent: bool = False


class Event(EventEntry):
    """A full event row including ecas's send state and derived schedule."""

    cancellation_flag: bool = False
    welcome_sent: bool = False
    thank_you_sent: bool = False
    cancellation_sent: bool = False
    schedule: list[EmailSchedule] = Field(default_factory=list)


class PayrollUser(BaseModel):
    """The user auth model."""

    id: str
    email: str
    name: str | None = None
