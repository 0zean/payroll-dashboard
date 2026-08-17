"""Sidebar component for the app."""

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState

NAV_ITEM_BASE = "nav-item focus-ring flex w-full items-center gap-2 rounded-xl px-3 py-2 text-sm font-medium"
NAV_ITEM_ACTIVE = f"{NAV_ITEM_BASE} nav-item-active bg-white/8 text-white"
NAV_ITEM_IDLE = (
    f"{NAV_ITEM_BASE} text-white/65 hover:bg-white/5 hover:text-white"
)


def sidebar_header() -> rx.Component:
    """Sidebar header.

    Returns:
        The sidebar header component.

    """
    return rx.hstack(
        rx.el.div(
            rx.icon("badge-dollar-sign", size=18, color="white"),
            class_name="brand-mark flex h-9 w-9 items-center justify-center rounded-xl",
        ),
        rx.vstack(
            rx.el.span(
                "Payroll",
                class_name="text-sm font-semibold tracking-tight text-white",
            ),
            rx.el.span(
                "Operations cockpit",
                class_name="text-[11px] font-medium uppercase tracking-[0.14em] text-white/40",
            ),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        align="center",
        width="100%",
        padding="0.35em",
        margin_bottom="1.25em",
    )


def sidebar_footer() -> rx.Component:
    """Sidebar footer.

    Returns:
        The sidebar footer component.

    """
    return rx.el.div(
        rx.hstack(
            rx.link(
                rx.text("Docs", size="2"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                color_scheme="gray",
                underline="none",
                class_name="text-white/45 transition-colors duration-200 hover:text-white",
            ),
            rx.link(
                rx.text("Blog", size="2"),
                href="https://reflex.dev/blog/",
                color_scheme="gray",
                underline="none",
                class_name="text-white/45 transition-colors duration-200 hover:text-white",
            ),
            rx.spacer(),
            rx.el.span("Dark mode", class_name="text-xs text-white/45"),
            justify="start",
            align="center",
            width="100%",
        ),
        class_name="w-full border-t border-white/8 px-1 pt-3",
    )


def sidebar_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=17)


def sidebar_item(
    text: str,
    url: str = "",
    on_click: rx.event.EventType | None = None,
) -> rx.Component:
    """Sidebar item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The sidebar item component.

    """
    # Whether the item is active.
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & text == "Overview"
    )

    return rx.link(
        rx.el.div(
            rx.match(
                text,
                ("Overview", sidebar_item_icon("home")),
                ("Table", sidebar_item_icon("table-2")),
                ("Onboard", sidebar_item_icon("user-plus")),
                ("Settings", sidebar_item_icon("settings")),
                ("Logout", sidebar_item_icon("log-out")),
                sidebar_item_icon("layout-dashboard"),
            ),
            rx.el.span(text),
            class_name=rx.cond(active, NAV_ITEM_ACTIVE, NAV_ITEM_IDLE),
        ),
        underline="none",
        href=url,
        width="100%",
        on_click=on_click,
    )


def sidebar() -> rx.Component:
    """The sidebar.

    Returns:
        The sidebar component.
    """
    from reflex.page import DECORATED_PAGES

    ordered_page_routes = [
        "/",
        "/table",
        "/onboard",
        "/settings",
    ]

    pages = [
        page_dict
        for page_list in DECORATED_PAGES.values()
        for _, page_dict in page_list
    ]

    ordered_pages = sorted(
        pages,
        key=lambda page: (
            ordered_page_routes.index(page["route"])
            if page["route"] in ordered_page_routes
            else len(ordered_page_routes)
        ),
    )

    return rx.flex(
        rx.vstack(
            sidebar_header(),
            rx.el.p(
                "Navigation",
                class_name="px-2 pb-1 text-[10px] font-semibold uppercase tracking-[0.18em] text-white/35",
            ),
            rx.vstack(
                *[
                    sidebar_item(
                        text=page.get(
                            "title", page["route"].strip("/").capitalize()
                        ),
                        url=page["route"],
                    )
                    for page in ordered_pages
                ],
                spacing="1",
                width="100%",
            ),
            rx.spacer(),
            rx.vstack(
                sidebar_item("Logout", on_click=AuthState.logout()),  # type: ignore
                sidebar_footer(),
                spacing="3",
                width="100%",
            ),
            justify="start",
            align="start",
            width=styles.sidebar_content_width,
            height="100dvh",
            padding="1.25em 1em",
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
        class_name="glass-panel border-y-0 border-l-0 border-r border-white/8",
        background="linear-gradient(180deg, rgba(255,255,255,0.045), rgba(255,255,255,0.012))",
    )
