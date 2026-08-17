"""Material 3 light/dark scheme toggle used in the navigation shell."""

import reflex as rx

from payroll_dashboard.states.theme_state import ThemeState


def theme_toggle(show_label: bool = True) -> rx.Component:
    """An M3 icon button (optionally with a label) toggling the color scheme.

    Args:
        show_label: Whether to render the trailing text label.

    Returns:
        The toggle component.
    """
    return rx.el.button(
        rx.cond(
            ThemeState.is_dark,
            rx.icon("sun", size=18),
            rx.icon("moon", size=18),
        ),
        rx.cond(
            show_label,
            rx.el.span(
                rx.cond(ThemeState.is_dark, "Light mode", "Dark mode"),
                class_name="md-label-large",
            ),
            rx.fragment(),
        ),
        on_click=ThemeState.toggle_appearance,
        aria_label="Toggle color scheme",
        type="button",
        class_name=(
            "md-press focus-ring md-state-layer flex items-center gap-2 rounded-full "
            "px-3 py-2 md-on-surface-variant hover:md-on-surface"
        ),
    )
