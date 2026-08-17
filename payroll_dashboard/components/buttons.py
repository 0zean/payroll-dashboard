import reflex as rx
from reflex.event import EventCallback
from reflex_components_radix.themes.base import LiteralAccentColor


ACTION_BUTTON_CLASS = "md-press focus-ring"

ACTION_BUTTON_STYLE = {
    "border": "none",
    "border_radius": "var(--md-sys-shape-corner-full)",
    "box_shadow": "var(--md-sys-elevation-level1)",
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
                class_name="md-headline-small md-on-surface",
            ),
            rx.alert_dialog.description(
                "Are you sure? This will clear all hours and pay from the Master list in Sheets.",
                size="2",
                class_name="md-body-medium md-on-surface-variant",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="ghost",
                        color_scheme="gray",
                        radius="full",
                        class_name=f"{ACTION_BUTTON_CLASS} md-label-large",
                    ),
                ),
                rx.alert_dialog.action(
                    rx.button(
                        "Yes, Delete",
                        color_scheme="red",
                        variant="solid",
                        radius="full",
                        on_click=event,
                        class_name=f"{ACTION_BUTTON_CLASS} md-label-large",
                    ),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
            style={"max_width": 450},
            class_name="md-dialog",
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
