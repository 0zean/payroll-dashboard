"""The onboarding page."""

import reflex as rx

from payroll_dashboard.components.form_field import form_field

from ..backend.onboard_state import OnboardingState
from ..templates import template

TACTILE_CLASS = "press focus-ring"
EYEBROW_CLASS = (
    "text-[10px] font-semibold uppercase tracking-[0.22em] text-white/40"
)
HINT_CLASS = "text-[13px] font-medium leading-relaxed text-white/50"


def onboard_hero() -> rx.Component:
    """Page heading block for the onboarding screen."""
    return rx.el.div(
        rx.el.p("Employee lifecycle", class_name=EYEBROW_CLASS),
        rx.heading(
            "Employee Onboarding",
            size="6",
            class_name="tracking-tight text-white",
        ),
        rx.el.p(
            "Register a new employee and their hourly rate. Onboarded names become "
            "selectable in payroll entry immediately.",
            class_name=f"{HINT_CLASS} max-w-[46ch]",
        ),
        class_name="flex w-full flex-col gap-2",
    )


def onboard_checklist() -> rx.Component:
    """Side panel summarizing what happens after onboarding."""
    return rx.el.div(
        rx.el.p("What happens next", class_name=EYEBROW_CLASS),
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
            "glass-card spotlight flex w-full flex-col gap-4 rounded-2xl p-5 "
            "lg:max-w-[22rem]"
        ),
    )


def _checklist_item(icon: str, title: str, body: str) -> rx.Component:
    return rx.el.li(
        rx.el.div(
            rx.icon(icon, size=15, color="white"),
            class_name=(
                "mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg "
                "border border-white/10 bg-white/5"
            ),
        ),
        rx.el.div(
            rx.el.span(
                title,
                class_name="text-[13px] font-semibold text-white",
            ),
            rx.el.span(body, class_name="text-[12px] text-white/45"),
            class_name="flex flex-col gap-0.5",
        ),
        class_name="flex items-start gap-3",
    )


def onboard_form() -> rx.Component:
    """The onboarding form card."""
    return rx.el.div(
        rx.el.div(
            rx.badge(
                rx.icon(tag="user-plus", size=22),
                color_scheme="grass",
                variant="soft",
                radius="full",
                padding="0.6rem",
                class_name="shrink-0",
            ),
            rx.el.div(
                rx.el.span(
                    "Add New Employee",
                    class_name="text-base font-semibold tracking-tight text-white",
                ),
                rx.el.span(
                    "All fields are required.",
                    class_name="text-[12px] font-medium text-white/45",
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
                ),
                form_field(
                    label="Pay Rate (per hour)",
                    name="pay_rate",
                    placeholder="Enter hourly pay rate",
                    type="number",
                    icon="dollar-sign",
                    required=True,
                ),
                class_name="grid w-full grid-cols-1 gap-4 sm:grid-cols-2",
            ),
            rx.el.div(
                rx.link(
                    "Go to Payroll Entry",
                    href="/table",
                    underline="none",
                    class_name=(
                        "focus-ring text-sm font-semibold text-[#A5AEFF] "
                        "transition-colors duration-200 hover:text-white"
                    ),
                ),
                rx.button(
                    rx.icon("user-plus", size=16),
                    "Add Employee",
                    type="submit",
                    size="3",
                    variant="surface",
                    loading=OnboardingState.loading,
                    class_name=f"{TACTILE_CLASS} w-full font-semibold sm:w-auto",
                ),
                class_name=(
                    "mt-2 flex w-full flex-col items-stretch gap-3 border-t border-white/8 "
                    "pt-5 sm:flex-row sm:items-center sm:justify-between"
                ),
            ),
            on_submit=OnboardingState.start_onboard,
            class_name="flex w-full flex-col gap-5",
        ),
        class_name=(
            "glass-card spotlight flex w-full flex-1 flex-col gap-6 rounded-2xl p-5 sm:p-7"
        ),
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
