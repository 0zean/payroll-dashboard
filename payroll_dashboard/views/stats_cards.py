import reflex as rx
from reflex_components_radix.themes.base import LiteralAccentColor

from .. import styles
from ..backend.table_state import TableState


def stats_card(
    stat_name: str,
    value: float,
    icon: str,
    icon_color: LiteralAccentColor,
    extra_char: str = "",
) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.badge(
                rx.icon(tag=icon, size=22),
                color_scheme=icon_color,
                variant="soft",
                radius="full",
                padding="0.65rem",
                class_name="shrink-0",
            ),
            rx.vstack(
                rx.el.span(
                    stat_name,
                    class_name=(
                        "text-[10px] font-semibold uppercase tracking-[0.16em] text-white/45"
                    ),
                ),
                rx.el.span(
                    f"{extra_char}{value:,}",
                    class_name=(
                        "tabular text-2xl font-semibold leading-tight tracking-tight text-white"
                    ),
                ),
                spacing="1",
                align="start",
                width="100%",
            ),
            spacing="3",
            align="center",
            width="100%",
        ),
        size="3",
        width="100%",
        box_shadow=styles.box_shadow_style,
        class_name="glass-card spotlight rounded-2xl",
    )


def stats_cards() -> rx.Component:
    return rx.grid(
        stats_card(
            stat_name="Total Entries",
            value=TableState.stats.total_entries,
            icon="notebook-pen",
            icon_color="blue",
        ),
        stats_card(
            stat_name="Total Hours",
            value=TableState.stats.total_hours,
            icon="hourglass",
            icon_color="green",
        ),
        stats_card(
            stat_name="Total Employees",
            value=TableState.stats.employees_count,
            icon="id-card",
            icon_color="purple",
        ),
        gap="1rem",
        grid_template_columns=[
            "minmax(0, 1fr)",
            "minmax(0, 1fr)",
            "repeat(2, minmax(0, 1fr))",
            "repeat(3, minmax(0, 1fr))",
            "repeat(3, minmax(0, 1fr))",
        ],
        width="100%",
    )
