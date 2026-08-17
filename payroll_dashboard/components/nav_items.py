"""Shared navigation metadata + item builders for the M3 navigation shell."""

import reflex as rx

NAV_ORDER = ["/", "/table", "/onboard", "/settings"]

NAV_ITEM_BASE = "md-nav-item focus-ring w-full"
NAV_ITEM_ACTIVE = f"{NAV_ITEM_BASE} md-nav-item-active"


def ordered_pages() -> list[dict[str, str]]:
    """Registered pages sorted into the navigation order.

    Returns:
        A list of page dicts (route + optional title).
    """
    from reflex.page import DECORATED_PAGES

    pages = [
        page_dict
        for page_list in DECORATED_PAGES.values()
        for _, page_dict in page_list
    ]

    return sorted(
        pages,
        key=lambda page: (
            NAV_ORDER.index(page["route"])
            if page["route"] in NAV_ORDER
            else len(NAV_ORDER)
        ),
    )


def nav_icon(text: str, size: int = 20) -> rx.Component:
    """The leading icon for a navigation destination."""
    return rx.match(
        text,
        ("Overview", rx.icon("house", size=size)),
        ("Table", rx.icon("table-2", size=size)),
        ("Onboard", rx.icon("user-plus", size=size)),
        ("Settings", rx.icon("settings", size=size)),
        ("Logout", rx.icon("log-out", size=size)),
        rx.icon("layout-dashboard", size=size),
    )


def nav_item(
    text: str,
    url: str = "",
    on_click: rx.event.EventType | None = None,
) -> rx.Component:
    """An M3 navigation drawer destination.

    Args:
        text: The label of the destination.
        url: The route it points at.
        on_click: Optional extra event handler.

    Returns:
        The navigation item component.
    """
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & (text == "Overview")
    )

    return rx.link(
        rx.el.div(
            nav_icon(text),
            rx.el.span(text, class_name="md-label-large"),
            class_name=rx.cond(active, NAV_ITEM_ACTIVE, NAV_ITEM_BASE),
        ),
        underline="none",
        href=url,
        width="100%",
        on_click=on_click,
    )
