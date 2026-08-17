import reflex as rx

from payroll_dashboard.states.theme_state import ThemeState

PICKER_SELECT_CLASS = "md-press focus-ring w-full sm:max-w-[16rem]"


def radius_picker() -> rx.Component:
    return rx.el.div(
        rx.select(
            [
                "none",
                "small",
                "medium",
                "large",
                "full",
            ],
            size="3",
            radius="large",
            value=ThemeState.radius,
            on_change=ThemeState.set_radius,  # type: ignore
            class_name=PICKER_SELECT_CLASS,
        ),
        rx.el.p(
            "Current:",
            rx.el.strong(ThemeState.radius),
            class_name="md-value-chip",
        ),
        class_name="flex w-full flex-col items-start gap-3",
    )
