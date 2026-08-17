import reflex as rx


def card(*children, **props):
    """An M3 elevated card. Elevation and shape come from the M3 component sheet."""
    return rx.card(
        *children,
        size="3",
        width="100%",
        **props,
    )
