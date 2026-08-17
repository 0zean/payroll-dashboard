import reflex as rx
from reflex.event import EventCallback

from .icon import icon


def clean_button(
    icon_tag: str,
    event: EventCallback[*tuple[()]],
    loading: bool,
) -> rx.Component:
    """Destructive action guarded by an M3 alert dialog."""
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.icon_button(
                icon(icon_tag, size=24),
                variant="soft",
                size="3",
                loading=loading,
                aria_label="Clean master list",
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title("Clean Master List"),
            rx.alert_dialog.description(
                "Are you sure? This will clear all hours and pay from the Master list in Sheets.",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button("Cancel", variant="ghost", color_scheme="gray"),
                ),
                rx.alert_dialog.action(
                    # M3 keeps destructive confirmations as text buttons in the error colour.
                    rx.button("Clear list", variant="ghost", color_scheme="tomato", on_click=event),
                ),
                spacing="2",
                margin_top="24px",
                justify="end",
            ),
            style={"max_width": 450},
        ),
    )


def download_button(
    icon_tag: str,
    hint: str,
    event: EventCallback[*tuple[()]],
    loading: bool,
) -> rx.Component:
    return rx.tooltip(
        rx.icon_button(
            icon(icon_tag, size=24),
            variant="soft",
            size="3",
            on_click=event,
            loading=loading,
            aria_label=hint,
        ),
        content=hint,
    )
