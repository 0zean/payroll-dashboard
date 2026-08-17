"""The onboarding page."""

import reflex as rx

from ..backend.onboard_state import OnboardingState
from ..components.form_field import form_field
from ..components.icon import icon
from ..templates import template

# What submitting the form actually does, so the outcome is visible up front.
NEXT_STEPS = (
    (
        "user-plus",
        "Added to the Master List",
        "The employee is appended to the payroll masterlist in Sheets.",
    ),
    (
        "dollar-sign",
        "Pay rate stored",
        "The hourly rate is used when payroll hours are synced.",
    ),
    (
        "checklist",
        "Ready for entry",
        "The name appears in the employee selector on the table page.",
    ),
)


def _eyebrow(text: str) -> rx.Component:
    return rx.text(
        text,
        font="var(--md-sys-typescale-label-medium)",
        letter_spacing="0.1em",
        text_transform="uppercase",
        color="var(--md-sys-color-on-surface-variant)",
    )


def _tonal_icon(icon_tag: str, size: str = "3rem", radius: str = "var(--md-sys-shape-corner-full)") -> rx.Component:
    return rx.flex(
        icon(icon_tag, size=24, color="var(--md-sys-color-on-secondary-container)"),
        background="var(--md-sys-color-secondary-container)",
        border_radius=radius,
        min_width=size,
        height=size,
        align="center",
        justify="center",
    )


def _next_step(icon_tag: str, title: str, description: str) -> rx.Component:
    return rx.hstack(
        _tonal_icon(icon_tag, size="2.25rem", radius="var(--md-sys-shape-corner-small)"),
        rx.vstack(
            rx.text(
                title,
                font="var(--md-sys-typescale-title-small)",
                letter_spacing="var(--md-sys-typescale-title-small-tracking)",
            ),
            rx.text(
                description,
                font="var(--md-sys-typescale-body-small)",
                letter_spacing="var(--md-sys-typescale-body-small-tracking)",
                color="var(--md-sys-color-on-surface-variant)",
            ),
            spacing="1",
            align_items="start",
        ),
        spacing="3",
        align="start",
        width="100%",
    )


def what_happens_next() -> rx.Component:
    """M3 outlined card explaining the effect of submitting the form."""
    return rx.card(
        rx.vstack(
            _eyebrow("What happens next"),
            *[_next_step(*step) for step in NEXT_STEPS],
            spacing="5",
            align_items="start",
            width="100%",
        ),
        variant="ghost",
        size="4",
        width="100%",
    )


def _onboard_form() -> rx.Component:
    return rx.card(
        rx.form(
            rx.hstack(
                _tonal_icon("user-plus"),
                rx.vstack(
                    rx.text(
                        "Add New Employee",
                        font="var(--md-sys-typescale-title-large)",
                    ),
                    rx.text(
                        "Fields marked with * are required.",
                        font="var(--md-sys-typescale-body-medium)",
                        color="var(--md-sys-color-on-surface-variant)",
                    ),
                    spacing="0",
                    align_items="start",
                ),
                align="center",
                spacing="4",
                width="100%",
                margin_bottom="1.5em",
            ),
            rx.flex(
                form_field(
                    label="Name",
                    name="employee_name",
                    placeholder="Enter employee name",
                    type="text",
                    icon_tag="user-plus",
                    required=True,
                    helper="Full name as it should appear in the Master List.",
                ),
                form_field(
                    label="Pay Rate (per hour)",
                    name="pay_rate",
                    placeholder="Enter hourly pay rate",
                    type="number",
                    icon_tag="dollar-sign",
                    required=True,
                    helper="Hourly rate used to calculate payroll totals.",
                ),
                direction=rx.breakpoints(initial="column", sm="row"),
                gap="1.5rem",
                width="100%",
            ),
            rx.divider(margin_y="1.5rem", color="var(--md-sys-color-outline-variant)"),
            rx.hstack(
                rx.link("Go to Payroll Entry", href="/table"),
                rx.button(
                    icon("user-plus", size=20),
                    "Add Employee",
                    type="submit",
                    size="3",
                    loading=OnboardingState.loading,
                ),
                width="100%",
                justify="between",
                align="center",
            ),
            display="flex",
            flex_direction="column",
            on_submit=OnboardingState.start_onboard,
        ),
        size="4",
        width="100%",
    )


@template(route="/onboard", title="Onboard")
def onboard() -> rx.Component:
    """The onboarding page.

    Returns:
        The UI for the onboarding page.

    """
    return rx.vstack(
        rx.vstack(
            _eyebrow("Employee lifecycle"),
            rx.heading("Employee Onboarding", size="7"),
            rx.text(
                "Register a new employee and their hourly rate. Onboarded names become "
                "selectable in payroll entry immediately.",
                font="var(--md-sys-typescale-body-medium)",
                color="var(--md-sys-color-on-surface-variant)",
                max_width="46ch",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        # Grid rather than flex: a flex-basis is a *height* once the container
        # wraps to a column, which left dead space above the second card.
        rx.grid(
            _onboard_form(),
            what_happens_next(),
            grid_template_columns=[
                "minmax(0, 1fr)",
                "minmax(0, 1fr)",
                "minmax(0, 1fr)",
                "minmax(0, 1fr)",
                "minmax(0, 1fr) 20rem",
                "minmax(0, 1fr) 22rem",
            ],
            gap="1.5rem",
            # Stretch so both cards share the row height and their bottom edges
            # line up. In the single-column layout each row sizes itself, so
            # this has no effect there.
            align="stretch",
            width="100%",
        ),
        spacing="6",
        width="100%",
    )
