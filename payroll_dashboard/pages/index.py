"""The overview page of the app."""

import reflex as rx

from .. import styles
from ..backend.auth_state import AuthState
from ..backend.index_state import IndexState
from ..backend.table_state import TableState
from ..components.buttons import clean_button, download_button
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
        rx.el.div(
            rx.el.p("Payroll operations", class_name="md-eyebrow"),
            rx.el.h1(
                f"Welcome, {AuthState.user.name.split(' ')[0]}",  # type: ignore
                class_name="md-headline-small md-on-surface",
            ),
            rx.el.p(
                "Review payroll totals, clean the master list and sync the latest "
                "entries to Sheets.",
                class_name="md-supporting max-w-[62ch]",
            ),
            class_name="flex w-full flex-col gap-1",
        ),
        rx.el.div(
            rx.input(
                rx.input.slot(rx.icon("search", size=16), padding_left="0"),
                placeholder="Search here...",
                size="3",
                width="100%",
                radius="large",
                style=styles.ghost_input_style,
                class_name="w-full sm:max-w-[420px]",
            ),
            rx.el.div(
                clean_button(
                    "brush-cleaning",
                    "cyan",
                    event=IndexState.start_clean,
                    loading=IndexState.clear_loading,
                ),
                download_button(
                    "download",
                    "plum",
                    "Download Master List",
                    event=IndexState.start_download,
                    loading=IndexState.download_loading,
                ),
                class_name="flex shrink-0 items-center justify-start gap-3 sm:justify-end",
            ),
            class_name=(
                "md-toolbar md-elevate flex w-full flex-col gap-3 p-3 "
                "sm:flex-row sm:items-center sm:justify-between"
            ),
        ),
        stats_cards(),
        rx.vstack(
            rx.el.div(
                rx.link(
                    "Go to Payroll Entry",
                    href="/table",
                    underline="none",
                    class_name="md-button-text focus-ring",
                ),
                rx.button(
                    rx.icon("sheet", size=16),
                    rx.el.span("Sync to Sheets", class_name="md-label-large"),
                    type="submit",
                    size="3",
                    variant="soft",
                    radius="full",
                    loading=TableState.loading,
                    on_click=TableState.start_sync,
                    disabled=rx.cond(
                        TableState.users.length() > 0, False, True
                    ),  # type: ignore
                    class_name="md-press focus-ring w-full sm:w-auto",
                ),
                class_name=(
                    "flex w-full flex-col items-stretch gap-3 sm:flex-row sm:items-center "
                    "sm:justify-between"
                ),
            ),
            card(overview_table()),
            spacing="4",
            width="100%",
        ),
        spacing="7",
        width="100%",
    )
