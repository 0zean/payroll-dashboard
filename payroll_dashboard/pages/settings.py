"""The settings page."""

import reflex as rx

from ..templates import template
from ..views.color_picker import primary_color_picker, secondary_color_picker
from ..views.radius_picker import radius_picker
from ..views.scaling_picker import scaling_picker

EYEBROW_CLASS = (
    "text-[10px] font-semibold uppercase tracking-[0.22em] text-white/40"
)
SECTION_TITLE_CLASS = "text-base font-semibold tracking-tight text-white"
SECTION_HINT_CLASS = "text-[13px] font-medium leading-relaxed text-white/50"


def settings_hero() -> rx.Component:
    """Page heading block for the settings screen."""
    return rx.el.div(
        rx.el.p("Appearance", class_name=EYEBROW_CLASS),
        rx.heading(
            "Settings",
            size="6",
            class_name="tracking-tight text-white",
        ),
        rx.el.p(
            "Tune the cockpit theme. Changes apply instantly across every page.",
            class_name=f"{SECTION_HINT_CLASS} max-w-[52ch]",
        ),
        class_name="flex w-full flex-col gap-2",
    )


def settings_section(
    icon: str,
    title: str,
    description: str,
    control: rx.Component,
) -> rx.Component:
    """A glass panel wrapping one group of theme controls."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, size=16, color="white"),
                class_name=(
                    "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg "
                    "border border-white/10 bg-white/5"
                ),
            ),
            rx.el.div(
                rx.el.h2(title, class_name=SECTION_TITLE_CLASS),
                rx.el.p(description, class_name=SECTION_HINT_CLASS),
                class_name="flex flex-col gap-0.5",
            ),
            class_name="flex w-full items-start gap-3",
        ),
        rx.el.div(
            control,
            class_name="w-full border-t border-white/8 pt-5",
        ),
        class_name=(
            "glass-card spotlight flex w-full flex-col gap-5 rounded-2xl p-5 sm:p-6"
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
        settings_section(
            "palette",
            "Primary color",
            "Drives buttons, links, focus rings and accent surfaces.",
            primary_color_picker(),
        ),
        settings_section(
            "blend",
            "Secondary color",
            "Sets the neutral gray scale used for panels and muted text.",
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
