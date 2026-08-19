"""The events table -- one row per event in the ecas sheet."""

import reflex as rx

from ..backend.events_state import EventsState
from ..backend.schemas import EmailSchedule, Event
from ..backend.utils import header_cell
from ..components.icon import icon
from .event_dialog import cancel_event_button, edit_event_button

# Column label per email type, so the chips read as words rather than keys.
EMAIL_LABELS = {
    "welcome": "Welcome",
    "thank_you": "Thank-you",
    "cancellation": "Cancelled",
}


def status_chip(entry: EmailSchedule) -> rx.Component:
    """A tonal chip for one email type. Inactive states hide themselves in CSS."""
    label = rx.match(
        entry.email_type,
        ("welcome", "Welcome"),
        ("thank_you", "Thank-you"),
        ("cancellation", "Cancelled"),
        entry.email_type,
    )
    return rx.tooltip(
        rx.el.span(
            label,
            class_name="m3-status-chip",
            custom_attrs={"data-status": entry.status},
        ),
        content=rx.match(
            entry.status,
            ("sent", "Already sent by ecas"),
            ("due", "Queued — goes out on the next ecas run"),
            ("scheduled", f"Scheduled for {entry.trigger_date}"),
            ("missed", "Send window closed without delivery"),
            "Not applicable",
        ),
    )


def _date_range(event: Event) -> rx.Component:
    return rx.vstack(
        rx.text(event.start_date, font="var(--md-sys-typescale-body-medium)"),
        rx.text(
            f"to {event.end_date}",
            font="var(--md-sys-typescale-body-small)",
            color="var(--md-sys-color-on-surface-variant)",
        ),
        spacing="0",
        align_items="start",
    )


def show_event(event: Event) -> rx.Component:
    return rx.table.row(
        rx.table.cell(
            rx.vstack(
                rx.text(event.event_name, font="var(--md-sys-typescale-body-medium)"),
                rx.text(
                    event.event_id,
                    font="var(--md-sys-typescale-body-small)",
                    color="var(--md-sys-color-on-surface-variant)",
                ),
                spacing="0",
                align_items="start",
            )
        ),
        rx.table.cell(_date_range(event)),
        rx.table.cell(
            rx.vstack(
                rx.text(event.location_name, font="var(--md-sys-typescale-body-medium)"),
                rx.text(
                    event.location_address,
                    font="var(--md-sys-typescale-body-small)",
                    color="var(--md-sys-color-on-surface-variant)",
                ),
                spacing="0",
                align_items="start",
            )
        ),
        rx.table.cell(
            rx.hstack(
                icon("group", size=18, color="var(--md-sys-color-on-surface-variant)"),
                rx.text(event.recipients.length()),
                spacing="2",
                align="center",
            )
        ),
        rx.table.cell(
            rx.hstack(
                rx.foreach(event.schedule, status_chip),
                spacing="1",
                wrap="wrap",
                align="center",
            )
        ),
        rx.table.cell(
            rx.hstack(
                edit_event_button(event),
                cancel_event_button(event),
                spacing="1",
            )
        ),
        align="center",
    )


def events_table() -> rx.Component:
    return rx.box(
        rx.table.root(
            rx.table.header(
                rx.table.row(
                    header_cell("Event", "event"),
                    header_cell("Dates", "calendar-days"),
                    header_cell("Location", "location_on"),
                    header_cell("Recipients", "group"),
                    header_cell("Emails", "mail"),
                    header_cell("Actions", "cog"),
                ),
            ),
            rx.table.body(rx.foreach(EventsState.filtered_events, show_event)),
            variant="surface",
            size="3",
            width="100%",
        ),
        rx.cond(
            EventsState.filtered_events.length() == 0,
            rx.center(
                rx.vstack(
                    icon("event_busy", size=32, color="var(--md-sys-color-on-surface-variant)"),
                    rx.text(
                        "No events yet",
                        font="var(--md-sys-typescale-title-medium)",
                    ),
                    rx.text(
                        "Add an event to schedule its welcome and thank-you emails.",
                        font="var(--md-sys-typescale-body-medium)",
                        color="var(--md-sys-color-on-surface-variant)",
                    ),
                    spacing="2",
                    align="center",
                ),
                padding="3rem 1rem",
                width="100%",
            ),
        ),
        width="100%",
    )
