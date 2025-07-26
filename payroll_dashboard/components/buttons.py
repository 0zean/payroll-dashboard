import reflex as rx
from reflex.components.radix.themes.base import LiteralAccentColor


def remote_button(icon: str, color: LiteralAccentColor, hint: str, alert_dialog: bool = False) -> rx.Component:
    if alert_dialog:
        return rx.alert_dialog.root(
            rx.alert_dialog.trigger(
                rx.icon_button(
                    rx.icon(icon), padding="0.5rem", radius="full", variant="soft", color_scheme=color, size="3"
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
                        rx.button("Yes, Delete", color_scheme="ruby", variant="solid"),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                style={"max_width": 450},
            ),
        )
    return rx.tooltip(
        rx.box(
            rx.icon_button(
                rx.icon(icon),
                padding="0.5rem",
                radius="full",
                variant="soft",
                color_scheme=color,
                size="3",
            ),
            position="relative",
        ),
        content=hint,
    )
