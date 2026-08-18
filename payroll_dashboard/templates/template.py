"""Common templates used between pages in the app."""

from __future__ import annotations

from collections.abc import Callable

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState
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


# Generated palettes available in assets/m3-theme.css. Keep in sync with
# SEEDS in scripts/gen_m3_theme.py; the first entry is the default.
SEEDS = ("teal", "purple", "blue", "green", "crimson")


class ThemeState(rx.State):
    """The state for the theme of the app."""

    seed: str = SEEDS[0]

    @rx.event
    def set_seed(self, value: str):
        """Select the M3 seed palette.

        Args:
            value: Seed name; ignored if it has no generated palette.

        """
        if value in SEEDS:
            self.seed = value


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
            return rx.flex(
                rx.cond(
                    ~AuthState.is_authenticated,
                    login_view(),
                    rx.flex(
                        navbar(),
                        sidebar(),
                        rx.flex(
                            rx.vstack(
                                page_content(),
                                width="100%",
                                **styles.template_content_style,  # type: ignore
                            ),
                            width="100%",
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
                    ),
                ),
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
                has_background=True,
                # Colour, radius and scaling all come from the M3 token layer;
                # the seed attribute selects which generated palette applies.
                custom_attrs={"data-m3-seed": ThemeState.seed},
            )

        ALL_PAGES.append(
            {
                "route": route,
            }
            | ({"title": title} if title is not None else {})
        )

        return theme_wrap()

    return decorator
