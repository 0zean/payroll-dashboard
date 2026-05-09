import reflex as rx
from reflex.event import EventCallback
from reflex_components_radix.themes.base import LiteralAccentColor


def clean_button(
    icon: str,
    color: LiteralAccentColor,
    event: EventCallback[*tuple[()]],
    loading: bool,
) -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.icon_button(
                rx.icon(icon),
                padding="0.5rem",
                radius="full",
                variant="soft",
                color_scheme=color,
                size="3",
                loading=loading,
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Clean Master List"),
            rx.alert_dialog.description(
                "Are you sure? This will clear all hours and pay from the Master list in Sheets.",
                size="2",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancel", variant="soft", color_scheme="gray"),
                ),
                rx.alert_dialog.action(
                    rx.button("Yes, Delete", color_scheme="ruby", variant="solid", on_click=event),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )


def download_button(
    icon: str,
    color: LiteralAccentColor,
    hint: str,
    event: EventCallback[*tuple[()]],
    loading: bool,
) -> rx.Component:
    return rx.tooltip(
        rx.box(
            rx.icon_button(
                rx.icon(icon),
                padding="0.5rem",
                radius="full",
                variant="soft",
                color_scheme=color,
                size="3",
                on_click=event,
                loading=loading,
            ),
            position="relative",
        ),
        content=hint,
    )
