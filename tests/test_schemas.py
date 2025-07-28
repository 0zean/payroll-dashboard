from payroll_dashboard.backend.schemas import Employee, EmployeeEntry, EmployeeOnboarding, PayrollStats, PayrollUser


def test_employee_model_defaults():
    emp = Employee(id=1, employee_name="Test", hours_worked=5, date="2024-06-01", extra=0.0, notes="")
    assert emp.extra == 0.0
    assert emp.notes == ""


def test_employee_entry_fields():
    entry = EmployeeEntry(employee_name="Test", hours_worked=8, date="2024-06-01", extra=1, notes="note")
    assert entry.employee_name == "Test"
    assert entry.extra == 1


def test_employee_onboarding_fields():
    onboard = EmployeeOnboarding(employee_name="Test", pay_rate=15.5)
    assert onboard.pay_rate == 15.5


def test_payroll_stats_fields():
    stats = PayrollStats(total_entries=2, total_hours=10, employees_count=1)
    assert stats.total_entries == 2


def test_payroll_user_optional_name():
    user = PayrollUser(id="abc", email="a@b.com")
    assert user.name is None
