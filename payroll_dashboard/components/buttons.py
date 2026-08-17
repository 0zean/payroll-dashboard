import reflex as rx
from reflex.event import EventCallback
from reflex_components_radix.themes.base import LiteralAccentColor


ACTION_BUTTON_CLASS = "press focus-ring"

ACTION_BUTTON_STYLE = {
    "border": "1px solid rgba(255, 255, 255, 0.1)",
    "box_shadow": "inset 0 1px 0 rgba(255,255,255,0.08), 0 14px 30px -20px rgba(2,2,3,0.9)",
}


def clean_button(
    icon: str,
    color: LiteralAccentColor,
    event: EventCallback[*tuple[()]],
    loading: bool,
) -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.icon_button(
                rx.icon(icon, size=18),
                padding="0.5rem",
                radius="full",
                variant="soft",
                color_scheme=color,
                size="3",
                loading=loading,
                class_name=ACTION_BUTTON_CLASS,
                style=ACTION_BUTTON_STYLE,
            ),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.title(
                "Clean Master List",
                class_name="text-white tracking-tight",
            ),
            rx.alert_dialog.description(
                "Are you sure? This will clear all hours and pay from the Master list in Sheets.",
                size="2",
                class_name="text-white/60",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        color_scheme="gray",
                        class_name=ACTION_BUTTON_CLASS,
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Yes, Delete",
                        color_scheme="ruby",
                        variant="solid",
                        on_click=event,
                        class_name=f"{ACTION_BUTTON_CLASS} font-semibold",
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
            class_name="glass-card rounded-2xl",
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
                rx.icon(icon, size=18),
                padding="0.5rem",
                radius="full",
                variant="soft",
                color_scheme=color,
                size="3",
                on_click=event,
                loading=loading,
                class_name=ACTION_BUTTON_CLASS,
                style=ACTION_BUTTON_STYLE,
            ),
            position="relative",
        ),
        content=hint,
    )
