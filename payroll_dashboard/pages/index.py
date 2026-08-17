"""The overview page of the app."""

import reflex as rx

from ..backend.auth_state import AuthState
from ..backend.index_state import IndexState
from ..backend.table_state import TableState
from ..components.buttons import clean_button, download_button
from ..components.card import card
from ..components.icon import icon
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
                rx.input.slot(icon("search", size=20), padding_left="0"),
                placeholder="Search here...",
                size="3",
                width="100%",
                max_width="450px",
            ),
            rx.flex(
                clean_button(
                    "brush-cleaning",
                    event=IndexState.start_clean,
                    loading=IndexState.clear_loading,
                ),
                download_button(
                    "download",
                    "Download Master List",
                    event=IndexState.start_download,
                    loading=IndexState.download_loading,
                ),
                spacing="3",
                wrap="nowrap",
                justify="end",
            ),
            justify="between",
            align="center",
            gap="1rem",
            width="100%",
        ),
        stats_cards(),
        rx.vstack(
            rx.hstack(
                rx.link("Go to Payroll Entry", href="/table"),
                rx.button(
                    icon("sheet", size=20),
                    "Sync to Sheets",
                    type="submit",
                    variant="soft",
                    size="3",
                    loading=TableState.loading,
                    on_click=TableState.start_sync,
                    disabled=rx.cond(TableState.users.length() > 0, False, True),  # type: ignore
                ),
                width="100%",
                justify="between",
                align="center",
            ),
            card(overview_table()),
            spacing="4",
            width="100%",
        ),
        spacing="8",
        width="100%",
    )
