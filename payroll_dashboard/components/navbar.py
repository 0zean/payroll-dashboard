"""Material 3 top app bar + modal navigation drawer for small screens."""

import reflex as rx

from ..backend.auth_state import AuthState
from .brand import brand
from .nav_items import nav_item, ordered_pages
from .theme_toggle import theme_toggle

ICON_BUTTON_CLASS = "md-icon-button md-press focus-ring shrink-0"


def modal_drawer() -> rx.Component:
    """The M3 modal navigation drawer, opened from the top app bar."""
    return rx.drawer.root(
        rx.drawer.trigger(
            rx.el.button(
                rx.icon("menu", size=20),
                class_name=ICON_BUTTON_CLASS,
                aria_label="Open navigation",
                type="button",
            ),
        ),
        rx.drawer.overlay(z_index="5", background_color="rgba(0, 0, 0, 0.32)"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.hstack(
                        brand(),
                        rx.spacer(),
                        rx.drawer.close(
                            rx.el.button(
                                rx.icon("x", size=20),
                                class_name=ICON_BUTTON_CLASS,
                                aria_label="Close navigation",
                                type="button",
                            ),
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                    ),
                    rx.el.p(
                        "Navigation",
                        class_name="md-nav-headline md-label-medium px-4 pt-2",
                    ),
                    *[
                        nav_item(
                            text=page.get(
                                "title", page["route"].strip("/").capitalize()
                            ),
                            url=page["route"],
                        )
                        for page in ordered_pages()
                    ],
                    nav_item("Logout", on_click=AuthState.logout()),  # type: ignore
                    rx.spacer(),
                    rx.el.div(
                        theme_toggle(),
                        class_name="md-divider w-full border-t pt-3",
                    ),
                    spacing="2",
                    width="100%",
                ),
                top="auto",
                left="auto",
                height="100%",
                width="20em",
                padding="1em 0.75em",
                class_name="md-nav-modal",
            ),
            width="100%",
        ),
        direction="right",
    )


def navbar() -> rx.Component:
    """The M3 top app bar.

    Returns:
        The navbar component.
    """
    return rx.el.nav(
        rx.hstack(
            brand(compact=True),
            rx.spacer(),
            theme_toggle(show_label=False),
            modal_drawer(),
            align="center",
            spacing="2",
            width="100%",
            padding_y="0.6em",
            padding_x=["1em", "1em", "2em"],
        ),
        display=["block", "block", "block", "block", "block", "none"],
        position="sticky",
        top="0px",
        z_index="5",
        class_name="md-top-app-bar w-full",
    )
