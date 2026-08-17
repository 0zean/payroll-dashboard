"""The table page."""

import reflex as rx

from ..backend.table_state import TableState
from ..templates import template
from ..views.table import main_table


@template(route="/table", title="Table", on_load=TableState.load_entries)  # type: ignore
def table() -> rx.Component:
    """The table page.

    Returns:
        The UI for the table page.

    """
    return rx.vstack(
        rx.el.div(
            rx.el.p("Payroll entry", class_name="md-eyebrow"),
            rx.el.h1(
                "Hours & Entries",
                class_name="md-headline-small md-on-surface",
            ),
            rx.el.p(
                "Add, edit and review payroll entries. Sort, search and paginate the "
                "masterlist without leaving the page.",
                class_name="md-supporting max-w-[62ch]",
            ),
            class_name="flex w-full flex-col gap-1",
        ),
        main_table(),
        spacing="6",
        width="100%",
    )
