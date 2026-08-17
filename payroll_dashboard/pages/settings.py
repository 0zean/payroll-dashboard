"""The settings page."""

import reflex as rx

from ..templates import template
from ..views.color_picker import primary_color_picker, secondary_color_picker
from ..views.radius_picker import radius_picker
from ..views.scaling_picker import scaling_picker
from ..components.theme_toggle import theme_toggle

SECTION_CARD_CLASS = (
    "md-card md-elevate flex w-full flex-col gap-5 "
    "rounded-[var(--md-sys-shape-corner-large)] p-5 sm:p-6"
)


def settings_hero() -> rx.Component:
    """Page heading block for the settings screen."""
    return rx.el.div(
        rx.el.p("Appearance", class_name="md-eyebrow"),
        rx.el.h1("Settings", class_name="md-headline-small md-on-surface"),
        rx.el.p(
            "Tune the payroll workspace theme. Changes apply instantly across "
            "every page.",
            class_name="md-supporting max-w-[62ch]",
        ),
        class_name="flex w-full flex-col gap-1",
    )


def settings_section(
    icon: str,
    title: str,
    description: str,
    control: rx.Component,
) -> rx.Component:
    """A tonal M3 card wrapping one group of theme controls."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, size=17),
                class_name="md-icon-container h-9 w-9",
            ),
            rx.el.div(
                rx.el.h2(title, class_name="md-title-medium md-on-surface"),
                rx.el.p(description, class_name="md-supporting"),
                class_name="flex flex-col gap-0.5",
            ),
            class_name="flex w-full items-start gap-3",
        ),
        rx.el.div(
            control,
            class_name="md-divider w-full border-t pt-5",
        ),
        class_name=SECTION_CARD_CLASS,
    )


def color_scheme_section() -> rx.Component:
    """Light / dark scheme control expressed with M3 roles."""
    return settings_section(
        "sun-moon",
        "Color scheme",
        "Switch between the light and dark Material 3 token sets.",
        rx.el.div(
            theme_toggle(),
            rx.el.p(
                "Focus indicators, surfaces and text roles adapt automatically.",
                class_name="md-supporting-text",
            ),
            class_name="flex w-full flex-col items-start gap-2",
        ),
    )


@template(route="/settings", title="Settings")
def settings() -> rx.Component:
    """The settings page.

    Returns:
        The UI for the settings page.

    """
    return rx.vstack(
        settings_hero(),
        color_scheme_section(),
        settings_section(
            "palette",
            "Primary color",
            "Drives buttons, links, focus rings and accent surfaces.",
            primary_color_picker(),
        ),
        settings_section(
            "blend",
            "Secondary color",
            "Sets the neutral scale used for panels and muted text.",
            secondary_color_picker(),
        ),
        rx.el.div(
            settings_section(
                "radius",
                "Radius",
                "Corner rounding applied to controls and panels.",
                radius_picker(),
            ),
            settings_section(
                "ruler",
                "Scaling",
                "Global size of typography and spacing tokens.",
                scaling_picker(),
            ),
            class_name="grid w-full grid-cols-1 gap-4 lg:grid-cols-2",
        ),
        spacing="5",
        width="100%",
    )
