"""M3 theme controls: seed palette and colour scheme."""

import reflex as rx
from reflex.style import set_color_mode

from ..components.icon import icon
from ..templates.template import SEEDS, ThemeState


def _swatch(name: str) -> rx.Component:
    active = ThemeState.seed == name
    return rx.tooltip(
        rx.box(
            rx.cond(active, icon("check", size=20, color="var(--md-sys-color-on-primary)")),
            background=f"var(--m3-seed-{name})",
            height="2.5rem",
            width="2.5rem",
            border_radius="var(--md-sys-shape-corner-full)",
            border=rx.cond(active, "3px solid var(--md-sys-color-on-surface)", "3px solid transparent"),
            cursor="pointer",
            display="flex",
            align_items="center",
            justify_content="center",
            transition="transform 150ms var(--md-sys-motion-easing-emphasized)",
            _hover={"transform": "scale(1.08)"},
            _active={"transform": "scale(0.95)"},
            on_click=ThemeState.set_seed(name),
            role="radio",
            aria_checked=active.to_string(),
            aria_label=name.capitalize(),
        ),
        content=name.capitalize(),
    )


def theme_picker() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.hstack(
                icon("palette", size=24, color="var(--md-sys-color-primary)"),
                rx.heading("Palette", size="6"),
                align="center",
                spacing="2",
            ),
            rx.text(
                "Every colour in the app is generated from this seed.",
                size="2",
                color="var(--md-sys-color-on-surface-variant)",
            ),
            rx.flex(
                *[_swatch(name) for name in SEEDS],
                gap="1rem",
                wrap="wrap",
                role="radiogroup",
                aria_label="Palette seed",
                padding_top="0.5rem",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        rx.vstack(
            rx.hstack(
                icon("blend", size=24, color="var(--md-sys-color-primary)"),
                rx.heading("Appearance", size="6"),
                align="center",
                spacing="2",
            ),
            rx.segmented_control.root(
                rx.segmented_control.item("Light", value="light"),
                rx.segmented_control.item("Dark", value="dark"),
                rx.segmented_control.item("System", value="system"),
                value=rx.color_mode,
                on_change=set_color_mode,
                size="3",
            ),
            spacing="3",
            align_items="start",
            width="100%",
        ),
        spacing="7",
        width="100%",
    )
