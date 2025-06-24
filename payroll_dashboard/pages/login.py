"""The login page."""


import reflex as rx

from ..components.login import login_default
from ..templates import template


@template(route="/login", title="Login")
def login() -> rx.Component:
    """The login page.

    Returns:
        The UI for the login page.
    """
    return rx.vstack(
        rx.heading("user", size="5"),
        login_default(),
        spacing="8",
        width="100%",
    )