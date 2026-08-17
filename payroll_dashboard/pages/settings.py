"""The settings page."""

import reflex as rx

from ..templates import template
from ..views.theme_picker import theme_picker


@template(route="/settings", title="Settings")
def settings() -> rx.Component:
    """The settings page.

    Returns:
        The UI for the settings page.

    """
    return rx.vstack(
        rx.heading("Settings", size="5"),
        theme_picker(),
        spacing="7",
        width="100%",
    )
