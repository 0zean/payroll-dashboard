import reflex as rx

from .api_routes import onboard_employee
from .schemas import EmployeeOnboarding
from .table_state import TableState


class OnboardingState(rx.State):
    onboarding: EmployeeOnboarding = EmployeeOnboarding(employee_name="", pay_rate=0)
    loading: bool = False

    @rx.event
    async def start_onboard(self, form_data: dict):
        self.onboarding = EmployeeOnboarding(**form_data)
        self.loading = True
        yield type(self).finish_onboard()

    @rx.event
    async def finish_onboard(self):
        try:
            await onboard_employee(self.onboarding)
            self.loading = False
            yield rx.toast.success("Onboarding updated successfully", position="top-center")
            yield TableState.set_employee_names()
        except Exception as e:
            self.loading = False
            yield rx.toast.error(f"Error onboarding employee: {e}", position="top-center")
