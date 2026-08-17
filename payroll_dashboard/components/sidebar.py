"""M3 navigation drawer for the app."""

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState
from .icon import icon

# Route -> (label, icon). Drives both the drawer and the mobile modal drawer.
NAV_ITEMS = [
    ("/", "Overview", "home"),
    ("/table", "Table", "table-2"),
    ("/onboard", "Onboard", "user-plus"),
    ("/settings", "Settings", "settings"),
]


def sidebar_header() -> rx.Component:
    """Drawer header.

    Returns:
        The drawer header component.

    """
    return rx.hstack(
        rx.color_mode_cond(
            rx.image(src="/reflex_black.svg", height="1.5em"),
            rx.image(src="/reflex_white.svg", height="1.5em"),
        ),
        rx.spacer(),
        align="center",
        width="100%",
        padding="0 16px",
        height="64px",
        flex_shrink="0",
    )


def sidebar_footer() -> rx.Component:
    """Drawer footer.

    Returns:
        The drawer footer component.

    """
    return rx.hstack(
        rx.link(
            rx.text("Docs", size="2"),
            href="https://reflex.dev/docs/getting-started/introduction/",
            underline="none",
            color="var(--md-sys-color-on-surface-variant)",
        ),
        rx.link(
            rx.text("Blog", size="2"),
            href="https://reflex.dev/blog/",
            underline="none",
            color="var(--md-sys-color-on-surface-variant)",
        ),
        rx.spacer(),
        rx.color_mode.button(style={"opacity": "0.8", "scale": "0.95"}),
        justify="start",
        align="center",
        width="100%",
        padding="0 12px",
    )


def nav_item(text: str, url: str = "", icon_tag: str = "layout-dashboard", on_click=None) -> rx.Component:
    """An M3 navigation drawer item: 56dp pill, tonal indicator when active.

    Args:
        text: The label.
        url: The route, when the item navigates.
        icon_tag: The Material Symbols icon.
        on_click: Event handler, for items that act instead of navigating.

    Returns:
        The navigation item component.

    """
    active = rx.State.router.page.path == url

    return rx.link(
        rx.hstack(
            icon(icon_tag, size=24, fill=active),
            rx.text(text, font="var(--md-sys-typescale-label-large)"),
            align="center",
            width="100%",
            spacing="3",
            height="56px",
            padding="0 24px",
            border_radius="var(--md-sys-shape-corner-full)",
            background_color=rx.cond(active, "var(--md-sys-color-secondary-container)", "transparent"),
            color=rx.cond(
                active,
                "var(--md-sys-color-on-secondary-container)",
                "var(--md-sys-color-on-surface-variant)",
            ),
            class_name="m3-nav-item",
        ),
        underline="none",
        href=url if not on_click else None,
        width="100%",
        on_click=on_click,
    )


def sidebar() -> rx.Component:
    """The navigation drawer.

    Returns:
        The drawer component.

    """
    return rx.flex(
        rx.vstack(
            sidebar_header(),
            rx.vstack(
                *[nav_item(text=label, url=route, icon_tag=tag) for route, label, tag in NAV_ITEMS],
                nav_item("Logout", icon_tag="log-out", on_click=AuthState.logout()),  # type: ignore
                spacing="1",
                width="100%",
            ),
            rx.spacer(),
            sidebar_footer(),
            align="start",
            width=styles.sidebar_content_width,
            height="100dvh",
            padding="0 12px 12px",
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
        background_color="var(--md-sys-color-surface-container-low)",
    )
