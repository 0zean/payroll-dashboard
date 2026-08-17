"""Common templates used between pages in the app."""

from __future__ import annotations

from typing import Callable

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState
from ..components.ambient import ambient_background
from ..components.navbar import navbar
from ..components.sidebar import sidebar
from ..views.login import login_view

# Meta tags for the app.
default_meta = [
    {
        "name": "viewport",
        "content": "width=device-width, shrink-to-fit=no, initial-scale=1",
    },
]


def menu_item_link(text, href):
    return rx.menu.item(
        rx.link(
            text,
            href=href,
            width="100%",
            color="inherit",
        ),
        _hover={
            "color": styles.accent_color,
            "background_color": styles.accent_text_color,
        },
    )


class ThemeState(rx.State):
    """The state for the theme of the app."""

    accent_color: str = "indigo"

    gray_color: str = "slate"

    radius: str = "large"

    scaling: str = "100%"


ALL_PAGES = []


def template(
    route: str | None = None,
    title: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[rx.Component] | None = None,
    on_load: rx.event.EventType[()] | None = None,
) -> Callable[[Callable[[], rx.Component]], rx.Component]:
    """The template for each page of the app.

    Args:
        route: The route to reach the page.
        title: The title of the page.
        description: The description of the page.
        meta: Additional meta to add to the page.
        on_load: The event handler(s) called when the page load.
        script_tags: Scripts to attach to the page.

    Returns:
        The template with the page content.

    """

    def decorator(page_content: Callable[[], rx.Component]) -> rx.Component:
        """The template for each page of the app.

        Args:
            page_content: The content of the page.

        Returns:
            The template with the page content.

        """
        # Get the meta tags for the page.
        all_meta = [*default_meta, *(meta or [])]

        def templated_page() -> rx.Component:
            return rx.el.div(
                rx.cond(
                    ~AuthState.is_authenticated,
                    login_view(),
                    rx.el.div(
                        ambient_background(),
                        rx.flex(
                            navbar(),
                            sidebar(),
                            rx.flex(
                                rx.vstack(
                                    page_content(),
                                    width="100%",
                                    class_name="rise-in",
                                    **styles.template_content_style,  # type: ignore
                                ),
                                width="100%",
                                min_width="0",
                                flex="1",
                                **styles.template_page_style,  # type: ignore
                                max_width=[
                                    "100%",
                                    "100%",
                                    "100%",
                                    "100%",
                                    "100%",
                                    styles.max_width,
                                ],
                            ),
                            flex_direction=[
                                "column",
                                "column",
                                "column",
                                "column",
                                "column",
                                "row",
                            ],
                            width="100%",
                            margin="auto",
                            position="relative",
                            z_index="1",
                        ),
                        class_name="app-canvas w-full",
                    ),
                ),
                class_name="min-h-screen w-full bg-[#020203] text-white",
            )

        @rx.page(
            route=route,
            title=title,
            description=description,
            meta=all_meta,
            script_tags=script_tags,
            on_load=on_load,
        )
        def theme_wrap() -> rx.Component:
            return rx.theme(
                templated_page(),
                appearance="dark",
                has_background=True,
                accent_color=ThemeState.accent_color,  # type: ignore
                gray_color=ThemeState.gray_color,  # type: ignore
                radius=ThemeState.radius,  # type: ignore
                scaling=ThemeState.scaling,  # type: ignore
            )

        ALL_PAGES.append(
            {
                "route": route,
            }
            | ({"title": title} if title is not None else {})
        )

        return theme_wrap()

    return decorator
