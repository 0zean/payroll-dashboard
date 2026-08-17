"""Ambient cinematic background layers used by the app shell."""

import reflex as rx


def ambient_background() -> rx.Component:
    """Layered gradient blobs, grid and noise overlays for the dark canvas.

    Returns:
        A fixed, non-interactive decorative layer.
    """
    return rx.el.div(
        rx.el.div(class_name="ambient-blob blob-indigo"),
        rx.el.div(class_name="ambient-blob blob-violet"),
        rx.el.div(class_name="ambient-blob blob-cyan"),
        rx.el.div(class_name="grid-overlay"),
        rx.el.div(class_name="noise-overlay"),
        rx.el.div(class_name="horizon-line"),
        class_name="ambient-layer",
        aria_hidden="true",
    )
