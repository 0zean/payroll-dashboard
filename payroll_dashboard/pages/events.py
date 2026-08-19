"""The events page -- manage the ecas events sheet."""

import reflex as rx

from ..backend.events_state import EventsState
from ..components.icon import icon
from ..templates import template
from ..views.event_dialog import add_event_button, event_form_dialog
from ..views.events_table import events_table


@template(route="/events", title="Events", on_load=EventsState.load_events)  # type: ignore
def events() -> rx.Component:
    """The events page.

    Returns:
        The UI for the events page.

    """
    return rx.vstack(
        rx.vstack(
            rx.text(
                "Event communications",
                font="var(--md-sys-typescale-label-medium)",
                letter_spacing="0.1em",
                text_transform="uppercase",
                color="var(--md-sys-color-on-surface-variant)",
            ),
            rx.heading("Events", size="7"),
            rx.text(
                "ecas sends welcome emails 2 days before an event starts and thank-you emails "
                "2 days before it ends. Marking an event cancelled queues a cancellation email "
                "for the next run.",
                font="var(--md-sys-typescale-body-medium)",
                color="var(--md-sys-color-on-surface-variant)",
                max_width="64ch",
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        rx.flex(
            add_event_button(),
            rx.spacer(),
            rx.input(
                rx.input.slot(icon("search", size=20)),
                placeholder="Search events...",
                size="3",
                max_width="280px",
                width="100%",
                value=EventsState.search_value,
                on_change=EventsState.set_search_value,
            ),
            rx.tooltip(
                rx.icon_button(
                    icon("refresh", size=20),
                    on_click=EventsState.load_events,
                    variant="ghost",
                    size="3",
                    loading=EventsState.loading,
                    aria_label="Reload events",
                ),
                content="Reload from the sheet",
            ),
            justify="end",
            align="center",
            spacing="3",
            wrap="wrap",
            width="100%",
        ),
        events_table(),
        event_form_dialog(),
        spacing="6",
        width="100%",
    )
