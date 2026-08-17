"""The onboarding page."""

import reflex as rx

from payroll_dashboard.components.form_field import form_field

from ..backend.onboard_state import OnboardingState
from ..templates import template

TACTILE_CLASS = "md-press focus-ring"
CARD_CLASS = (
    "md-card md-elevate flex w-full flex-col gap-6 "
    "rounded-[var(--md-sys-shape-corner-large)] p-5 sm:p-7"
)


def onboard_hero() -> rx.Component:
    """Page heading block for the onboarding screen."""
    return rx.el.div(
        rx.el.p("Employee lifecycle", class_name="md-eyebrow"),
        rx.el.h1(
            "Employee Onboarding",
            class_name="md-headline-small md-on-surface",
        ),
        rx.el.p(
            "Register a new employee and their hourly rate. Onboarded names become "
            "selectable in payroll entry immediately.",
            class_name="md-supporting max-w-[62ch]",
        ),
        class_name="flex w-full flex-col gap-1",
    )


def _checklist_item(icon: str, title: str, body: str) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.icon(icon, size=16),
            class_name="md-icon-container mt-0.5 h-8 w-8",
        ),
        rx.el.div(
            rx.el.span(title, class_name="md-title-small md-on-surface"),
            rx.el.span(body, class_name="md-body-small md-on-surface-variant"),
            class_name="flex flex-col gap-0.5",
        ),
        class_name="flex items-start gap-3",
    )


def onboard_checklist() -> rx.Component:
    """Side panel summarizing what happens after onboarding."""
    return rx.el.div(
        rx.el.p("What happens next", class_name="md-eyebrow"),
        rx.el.ul(
            _checklist_item(
                "user-check",
                "Added to the Master List",
                "The employee is appended to the payroll masterlist in Sheets.",
            ),
            _checklist_item(
                "dollar-sign",
                "Pay rate stored",
                "The hourly rate is used when payroll hours are synced.",
            ),
            _checklist_item(
                "list-checks",
                "Ready for entry",
                "The name appears in the employee selector on the table page.",
            ),
            class_name="flex flex-col gap-4",
        ),
        class_name=(
            "md-card-outlined md-elevate flex w-full flex-col gap-4 "
            "rounded-[var(--md-sys-shape-corner-large)] p-5 lg:max-w-[22rem]"
        ),
    )


def onboard_form() -> rx.Component:
    """The onboarding form card."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("user-plus", size=20),
                class_name="md-icon-container h-11 w-11 rounded-full",
            ),
            rx.el.div(
                rx.el.span(
                    "Add New Employee",
                    class_name="md-title-medium md-on-surface",
                ),
                rx.el.span(
                    "Fields marked with * are required.",
                    class_name="md-body-small md-on-surface-variant",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            class_name="flex w-full items-center gap-3",
        ),
        rx.form(
            rx.el.div(
                form_field(
                    label="Name",
                    name="employee_name",
                    placeholder="Enter employee name",
                    type="text",
                    icon="user-plus",
                    required=True,
                    supporting_text="Full name as it should appear in the Master List.",
                ),
                form_field(
                    label="Pay Rate (per hour)",
                    name="pay_rate",
                    placeholder="Enter hourly pay rate",
                    type="number",
                    icon="dollar-sign",
                    required=True,
                    supporting_text="Hourly rate used to calculate payroll totals.",
                ),
                class_name="grid w-full grid-cols-1 gap-5 sm:grid-cols-2",
            ),
            rx.el.div(
                rx.link(
                    "Go to Payroll Entry",
                    href="/table",
                    underline="none",
                    class_name="md-button-text focus-ring",
                ),
                rx.button(
                    rx.icon("user-plus", size=16),
                    rx.el.span("Add Employee", class_name="md-label-large"),
                    type="submit",
                    size="3",
                    variant="solid",
                    radius="full",
                    loading=OnboardingState.loading,
                    class_name=f"{TACTILE_CLASS} w-full sm:w-auto",
                ),
                class_name=(
                    "md-divider mt-1 flex w-full flex-col items-stretch gap-3 border-t "
                    "pt-5 sm:flex-row sm:items-center sm:justify-between"
                ),
            ),
            on_submit=OnboardingState.start_onboard,
            class_name="flex w-full flex-col gap-6",
        ),
        class_name=f"{CARD_CLASS} flex-1",
    )


@template(route="/onboard", title="Onboard")
def onboard() -> rx.Component:
    """The onboarding page.

    Returns:
        The UI for the onboarding page.

    """
    return rx.vstack(
        onboard_hero(),
        rx.el.div(
            onboard_form(),
            onboard_checklist(),
            class_name="flex w-full flex-col items-stretch gap-4 lg:flex-row",
        ),
        spacing="6",
        width="100%",
    )
