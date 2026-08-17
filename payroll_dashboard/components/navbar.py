"""Navbar component for the app."""

import reflex as rx

from ..backend.auth_state import AuthState

MENU_ITEM_BASE = "nav-item focus-ring flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-[15px] font-medium"
MENU_ITEM_ACTIVE = f"{MENU_ITEM_BASE} nav-item-active bg-white/8 text-white"
MENU_ITEM_IDLE = (
    f"{MENU_ITEM_BASE} text-white/65 hover:bg-white/5 hover:text-white"
)


def menu_item_icon(icon: str) -> rx.Component:
    return rx.icon(icon, size=19)


def menu_item(
    text: str,
    url: str = "",
    on_click: rx.event.EventType | None = None,
) -> rx.Component:
    """Menu item.

    Args:
        text: The text of the item.
        url: The URL of the item.

    Returns:
        rx.Component: The menu item component.

    """
    # Whether the item is active.
    active = (rx.State.router.page.path == url.lower()) | (
        (rx.State.router.page.path == "/") & text == "Overview"
    )

    return rx.link(
        rx.el.div(
            rx.match(
                text,
                ("Overview", menu_item_icon("home")),
                ("Table", menu_item_icon("table-2")),
                ("Onboard", menu_item_icon("user-plus")),
                ("Settings", menu_item_icon("settings")),
                ("Logout", menu_item_icon("log-out")),
                menu_item_icon("layout-dashboard"),
            ),
            rx.el.span(text),
            class_name=rx.cond(active, MENU_ITEM_ACTIVE, MENU_ITEM_IDLE),
        ),
        underline="none",
        href=url,
        width="100%",
        on_click=on_click,
    )


def navbar_footer() -> rx.Component:
    """Navbar footer.

    Returns:
        The navbar footer component.

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
        class_name="w-full border-t border-white/8 pt-3",
    )


def navbar_brand() -> rx.Component:
    return rx.hstack(
        rx.el.div(
            rx.icon("badge-dollar-sign", size=17, color="white"),
            class_name="brand-mark flex h-8 w-8 items-center justify-center rounded-lg",
        ),
        rx.vstack(
            rx.el.span(
                "Payroll",
                class_name="text-sm font-semibold tracking-tight text-white",
            ),
            rx.el.span(
                "Operations cockpit",
                class_name="text-[10px] font-medium uppercase tracking-[0.14em] text-white/40",
            ),
            spacing="0",
            align="start",
        ),
        align="center",
        spacing="3",
    )


def menu_button() -> rx.Component:
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

    return rx.drawer.root(
        rx.drawer.trigger(
            rx.el.button(
                rx.icon("align-justify", size=18, color="white"),
                class_name=(
                    "focus-ring press flex h-10 w-10 items-center justify-center rounded-xl "
                    "border border-white/10 bg-white/5 hover:bg-white/10"
                ),
                aria_label="Open navigation",
            ),
        ),
        rx.drawer.overlay(z_index="5", background_color="rgba(2, 2, 3, 0.72)"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.vstack(
                    rx.hstack(
                        navbar_brand(),
                        rx.spacer(),
                        rx.drawer.close(
                            rx.el.button(
                                rx.icon("x", size=17, color="white"),
                                class_name=(
                                    "focus-ring press flex h-9 w-9 items-center justify-center rounded-xl "
                                    "border border-white/10 bg-white/5 hover:bg-white/10"
                                ),
                                aria_label="Close navigation",
                            ),
                        ),
                        justify="between",
                        align="center",
                        width="100%",
                    ),
                    rx.el.p(
                        "Navigation",
                        class_name=(
                            "px-1 pt-2 text-[10px] font-semibold uppercase tracking-[0.18em] text-white/35"
                        ),
                    ),
                    *[
                        menu_item(
                            text=page.get(
                                "title", page["route"].strip("/").capitalize()
                            ),
                            url=page["route"],
                        )
                        for page in ordered_pages
                    ],
                    menu_item("Logout", on_click=AuthState.logout()),  # type: ignore
                    rx.spacer(),
                    navbar_footer(),
                    spacing="2",
                    width="100%",
                ),
                top="auto",
                left="auto",
                height="100%",
                width="20em",
                padding="1.25em 1em",
                background="linear-gradient(180deg, #08080b 0%, #020203 100%)",
                border_left="1px solid rgba(255,255,255,0.08)",
                class_name="backdrop-blur-xl",
            ),
            width="100%",
        ),
        direction="right",
    )


def navbar() -> rx.Component:
    """The navbar.

    Returns:
        The navbar component.

    """
    return rx.el.nav(
        rx.hstack(
            navbar_brand(),
            rx.spacer(),
            menu_button(),
            align="center",
            width="100%",
            padding_y="0.85em",
            padding_x=["1em", "1em", "2em"],
        ),
        display=["block", "block", "block", "block", "block", "none"],
        position="sticky",
        top="0px",
        z_index="5",
        class_name=(
            "w-full border-b border-white/8 bg-[#050506]/80 backdrop-blur-xl "
            "supports-[backdrop-filter]:bg-[#050506]/65"
        ),
    )
