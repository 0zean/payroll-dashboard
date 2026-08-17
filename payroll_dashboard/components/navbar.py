"""M3 top app bar and modal navigation drawer (compact windows)."""

import reflex as rx

from ..backend.auth_state import AuthState
from .icon import icon
from .sidebar import NAV_ITEMS, nav_item, sidebar_footer


def menu_button() -> rx.Component:
    """The modal navigation drawer, opened from the top app bar.

    Returns:
        The drawer component.

    """
    return rx.drawer.root(
        rx.drawer.trigger(
            rx.icon_button(
                icon("align-justify", size=24),
                variant="ghost",
                size="3",
                aria_label="Open navigation",
            ),
        ),
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.hstack(
                        rx.spacer(),
                        rx.drawer.close(
                            rx.icon_button(
                                icon("x", size=24),
                                variant="ghost",
                                size="3",
                                aria_label="Close navigation",
                            )
                        ),
                        justify="end",
                        width="100%",
                        height="64px",
                        align="center",
                    ),
                    *[nav_item(text=label, url=route, icon_tag=tag) for route, label, tag in NAV_ITEMS],
                    nav_item("Logout", icon_tag="log-out", on_click=AuthState.logout()),  # type: ignore
                    rx.spacer(),
                    sidebar_footer(),
                    spacing="1",
                    width="100%",
                    height="100%",
                ),
                top="auto",
                left="auto",
                height="100%",
                width="20em",
                padding="0 12px 12px",
                background_color="var(--md-sys-color-surface-container-low)",
                # M3 modal drawer: rounded on the inner edge only.
                border_radius="var(--md-sys-shape-corner-large) 0 0 var(--md-sys-shape-corner-large)",
            ),
            width="100%",
        ),
        direction="right",
    )


def navbar() -> rx.Component:
    """The M3 small top app bar.

    Returns:
        The top app bar component.

    """
    return rx.el.nav(
        rx.hstack(
            rx.color_mode_cond(
                rx.image(src="/reflex_black.svg", height="1em"),
                rx.image(src="/reflex_white.svg", height="1em"),
            ),
            rx.spacer(),
            menu_button(),
            align="center",
            width="100%",
            height="64px",
            padding_x=["1em", "1em", "2em"],
        ),
        display=["block", "block", "block", "block", "block", "none"],
        position="sticky",
        background_color="var(--md-sys-color-surface)",
        top="0px",
        z_index="5",
    )
