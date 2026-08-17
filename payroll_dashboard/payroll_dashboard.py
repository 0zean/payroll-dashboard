"""Welcome to Reflex!."""

# Import all the pages.
import reflex as rx

from . import styles
from .pages import *

# Create the app.
app = rx.App(
    style=styles.base_style,  # type: ignore
    stylesheets=styles.base_stylesheets,
    theme=rx.theme(
        appearance="light",
        accent_color="indigo",
        gray_color="slate",
        radius="large",
    ),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.meta(name="color-scheme", content="dark"),
        rx.el.meta(name="theme-color", content="#050506"),
    ],
)
