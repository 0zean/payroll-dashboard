"""Material 3 standard navigation drawer for the app shell."""

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState
from .brand import brand
from .nav_items import nav_item, ordered_pages
from .theme_toggle import theme_toggle


def drawer_headline() -> rx.Component:
    """Section headline above the destination list."""
    return rx.el.p(
        "Navigation",
        class_name="md-nav-headline md-label-medium px-4 pb-1 pt-2",
    )


def drawer_footer() -> rx.Component:
    """Footer with utility links and the scheme toggle."""
    return rx.el.div(
        theme_toggle(),
        rx.el.div(
            rx.link(
                "Docs",
                href="https://reflex.dev/docs/getting-started/introduction/",
                underline="none",
                class_name="md-label-large md-on-surface-variant hover:md-on-surface",
            ),
            rx.link(
                "Blog",
                href="https://reflex.dev/blog/",
                underline="none",
                class_name="md-label-large md-on-surface-variant hover:md-on-surface",
            ),
            class_name="flex items-center gap-4 px-4",
        ),
        class_name="md-divider flex w-full flex-col gap-2 border-t pt-3",
    )


def sidebar() -> rx.Component:
    """The M3 navigation drawer.

    Returns:
        The sidebar component.
    """
    return rx.flex(
        rx.vstack(
            rx.el.div(
                brand(),
                class_name="w-full px-3 pb-4 pt-1",
            ),
            drawer_headline(),
            rx.vstack(
                *[
                    nav_item(
                        text=page.get(
                            "title", page["route"].strip("/").capitalize()
                        ),
                        url=page["route"],
                    )
                    for page in ordered_pages()
                ],
                spacing="1",
                width="100%",
            ),
            rx.spacer(),
            rx.vstack(
                nav_item("Logout", on_click=AuthState.logout()),  # type: ignore
                drawer_footer(),
                spacing="3",
                width="100%",
            ),
            justify="start",
            align="start",
            width=styles.sidebar_content_width,
            height="100dvh",
            padding="1em 0.75em",
        ),
        display=["none", "none", "none", "none", "none", "flex"],
        max_width=styles.sidebar_width,
        width="auto",
        height="100%",
        position="sticky",
        justify="end",
        top="0px",
        left="0px",
        flex="1",
        z_index="2",
        class_name="md-nav-drawer",
    )
