import reflex as rx

from ..backend.table_state import TableState
from ..components.icon import icon


def stats_card(
    stat_name: str,
    value: float,
    icon_tag: str,
    role: str,
    extra_char: str = "",
) -> rx.Component:
    """An M3 elevated card with a tonal icon container.

    Args:
        stat_name: Label under the value.
        value: The statistic.
        icon_tag: Material Symbols icon.
        role: M3 container role ("primary", "secondary" or "tertiary").
        extra_char: Prefix for the value, e.g. a currency symbol.

    Returns:
        The stats card component.

    """
    return rx.card(
        rx.hstack(
            rx.flex(
                icon(icon_tag, size=24, color=f"var(--md-sys-color-on-{role}-container)"),
                background=f"var(--md-sys-color-{role}-container)",
                border_radius="var(--md-sys-shape-corner-full)",
                min_width="3rem",
                height="3rem",
                align="center",
                justify="center",
            ),
            rx.vstack(
                rx.text(
                    f"{extra_char}{value:,}",
                    font="var(--md-sys-typescale-headline-medium)",
                    color="var(--md-sys-color-on-surface)",
                ),
                rx.text(
                    stat_name,
                    font="var(--md-sys-typescale-body-medium)",
                    letter_spacing="var(--md-sys-typescale-body-medium-tracking)",
                    color="var(--md-sys-color-on-surface-variant)",
                ),
                spacing="0",
                align_items="start",
                width="100%",
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        size="4",
        width="100%",
    )


def stats_cards() -> rx.Component:
    return rx.grid(
        stats_card(
            stat_name="Total Entries",
            value=TableState.stats.total_entries,
            icon_tag="notebook-pen",
            role="primary",
        ),
        stats_card(
            stat_name="Total Hours",
            value=TableState.stats.total_hours,
            icon_tag="hourglass",
            role="secondary",
        ),
        stats_card(
            stat_name="Total Employees",
            value=TableState.stats.employees_count,
            icon_tag="id-card",
            role="tertiary",
        ),
        gap="1rem",
        grid_template_columns=[
            "1fr",
            "repeat(1, 1fr)",
            "repeat(2, 1fr)",
            "repeat(3, 1fr)",
            "repeat(3, 1fr)",
        ],
        width="100%",
    )
