import reflex as rx

from ..templates.template import ThemeState

PICKER_SELECT_CLASS = "press focus-ring w-full sm:max-w-[16rem]"


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
            "Current: ",
            rx.el.span(
                ThemeState.radius,
                class_name="font-semibold text-white",
            ),
            class_name="text-xs font-medium text-white/45",
        ),
        class_name="flex w-full flex-col gap-2",
    )
