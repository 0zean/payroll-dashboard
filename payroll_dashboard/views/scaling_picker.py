import reflex as rx

from ..templates.template import ThemeState

PICKER_SELECT_CLASS = "press focus-ring w-full sm:max-w-[16rem]"


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
            "Current: ",
            rx.el.span(
                ThemeState.scaling,
                class_name="tabular font-semibold text-white",
            ),
            class_name="text-xs font-medium text-white/45",
        ),
        class_name="flex w-full flex-col gap-2",
    )
