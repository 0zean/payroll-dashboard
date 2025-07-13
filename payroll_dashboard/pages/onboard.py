"""The onboarding page."""

import reflex as rx

from payroll_dashboard.components.form_field import form_field

from ..backend.onboard_state import OnboardingState
from ..templates import template


@template(route="/onboard", title="Onboard")
def onboard() -> rx.Component:
    """The onboarding page.

    Returns:
        The UI for the onboarding page.

    """
    return rx.box(
        rx.text(
            "Employee Onboarding",
            font_size="2.5rem",
            font_weight="bold",
            mb="2.5rem",
            mt="2.5rem",
            ml="3rem",
            align="left",
        ),
        rx.divider(margin="2rem 0"),
        rx.hstack(
            rx.form(
                rx.hstack(
                    rx.badge(
                        rx.icon(tag="user-plus", size=26),
                        color_scheme="grass",
                        radius="full",
                        padding="0.65rem",
                    ),
                    rx.text("Add New Employee", font_size="1.5rem", font_weight="bold"),
                    align="center",
                    justify="center",
                ),
                form_field(
                    label="Name",
                    name="employee_name",
                    placeholder="Enter employee name",
                    type="text",
                    icon="user-plus",
                    required=True,
                ),
                form_field(
                    label="Pay Rate (per hour)",
                    name="pay_rate",
                    placeholder="Enter hourly pay rate",
                    type="number",
                    icon="dollar-sign",
                    required=True,
                ),
                rx.hstack(
                    rx.box(
                        rx.link("Go to Payroll Entry", href="/table", font_weight="medium"),
                        align="start"
                    ),
                    rx.button(
                        "Add Employee",
                        align="end",
                        type="submit",
                        loading=OnboardingState.loading,
                    ),
                    width="100%",
                    justify="between",
                ),
                border_radius="1rem",
                p="2.5rem",
                width="40rem",
                display="flex",
                flex_direction="column",
                gap="0.5rem",
                on_submit=OnboardingState.start_onboard,
            ),
            width="100%",
            justify="center",
            position="center",
            align="center"
        ),
        # Link to return to Payroll Entry page
        min_h="100vh",
        position="relative",
        width="100%",
    )
