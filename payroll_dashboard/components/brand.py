"""Brand block used in the M3 navigation drawer and top app bar."""

import reflex as rx


def brand(compact: bool = False) -> rx.Component:
    """The app monogram plus wordmark.

    Args:
        compact: Render the tighter top-app-bar variant.

    Returns:
        The brand component.
    """
    gap_class = (
        "flex items-center gap-2" if compact else "flex items-center gap-3"
    )
    return rx.el.div(
        rx.el.div(
            rx.icon("badge-dollar-sign", size=20),
            class_name=(
                "md-brand-mark flex h-10 w-10 shrink-0 items-center justify-center "
                "rounded-full"
            ),
        ),
        rx.el.div(
            rx.el.span("Payroll", class_name="md-title-medium md-on-surface"),
            rx.el.span(
                "Operations",
                class_name="md-label-small md-on-surface-variant",
            ),
            class_name="flex flex-col",
        ),
        class_name=gap_class,
    )
