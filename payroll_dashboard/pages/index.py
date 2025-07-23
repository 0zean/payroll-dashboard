"""The overview page of the app."""

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState
from ..backend.table_state import TableState
from ..components.buttons import remote_button
from ..components.card import card
from ..templates import template
from ..views.overview_table import overview_table
from ..views.stats_cards import stats_cards


@template(route="/", title="Overview")  # type: ignore
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
                    loading=TableState.loading,
                    on_click=TableState.start_sync,
                    disabled=rx.cond(TableState.users.length()>0, False, True)  # type: ignore
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
