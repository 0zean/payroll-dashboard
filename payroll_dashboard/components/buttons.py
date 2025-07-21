import reflex as rx
from reflex.components.radix.themes.base import LiteralAccentColor


def remote_button(icon: str, color: LiteralAccentColor, hint: str) -> rx.Component:
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
