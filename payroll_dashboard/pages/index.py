"""The overview page of the app."""

import datetime

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState
from ..components.buttons import remote_button
from ..components.card import card
from ..templates import template
from ..views.charts import StatsState, area_toggle
from ..views.overview_table import overview_table
from ..views.stats_cards import stats_cards


def _time_data() -> rx.Component:
    return rx.hstack(
        rx.tooltip(
            rx.icon("info", size=20),
            content=f"{(datetime.datetime.now() - datetime.timedelta(days=30)).strftime('%b %d, %Y')} - {datetime.datetime.now().strftime('%b %d, %Y')}",
        ),
        rx.text("Last 30 days", size="4", weight="medium"),
        align="center",
        spacing="2",
        display=["none", "none", "flex"],
    )


def tab_content_header() -> rx.Component:
    return rx.hstack(
        _time_data(),
        area_toggle(),
        align="center",
        width="100%",
        spacing="4",
    )


@template(route="/", title="Overview", on_load=StatsState.randomize_data)  # type: ignore
def index() -> rx.Component:
    """The overview page.

    Returns:
        The UI for the overview page.

    """
    return rx.vstack(
        rx.heading(
            f"Welcome, {AuthState.user.name.split(' ')[0]}",  # type: ignore
            size="5",
        ),
        rx.flex(
            rx.input(
                rx.input.slot(rx.icon("search"), padding_left="0"),
                placeholder="Search here...",
                size="3",
                width="100%",
                max_width="450px",
                radius="large",
                style=styles.ghost_input_style,
            ),
            rx.flex(
                remote_button("brush-cleaning", "cyan", "Clean-up Master List"),
                remote_button("download", "plum", "Download Master List"),
                spacing="4",
                width="100%",
                wrap="nowrap",
                justify="end",
            ),
            justify="between",
            align="center",
            width="100%",
        ),
        stats_cards(),
        rx.vstack(
            rx.hstack(
                rx.box(rx.link("Go to Payroll Entry", href="/table", font_weight="medium"), align="start"),
                rx.button(
                    rx.icon("sheet"),
                    "Sync to Sheets",
                    align="end",
                    type="submit",
                ),
                width="100%",
                justify="between",
            ),
            card(overview_table()),
            width="100%",
        ),
        spacing="8",
        width="100%",
    )
