import reflex as rx

from payroll_dashboard.states.theme_state import ThemeState

PICKER_SELECT_CLASS = "md-press focus-ring w-full sm:max-w-[16rem]"


def scaling_picker() -> rx.Component:
    return rx.el.div(
        rx.select(
            [
                "90%",
                "95%",
                "100%",
                "105%",
                "110%",
            ],
            size="3",
            radius="large",
            value=ThemeState.scaling,
            on_change=ThemeState.set_scaling,  # type: ignore
            class_name=PICKER_SELECT_CLASS,
        ),
        rx.el.p(
            "Current:",
            rx.el.strong(ThemeState.scaling, class_name="tabular"),
            class_name="md-value-chip",
        ),
        class_name="flex w-full flex-col items-start gap-3",
    )
