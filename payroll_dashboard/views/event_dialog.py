"""Create/edit dialog and cancellation controls for events."""

import reflex as rx

from ..backend.events_state import EventsState
from ..backend.schemas import Event
from ..components.form_field import form_field
from ..components.icon import icon

UPLOAD_ID = "recipient_upload"


def _recipient_chip(email: str) -> rx.Component:
    """An M3 input chip with a trailing remove affordance."""
    return rx.el.span(
        email,
        rx.el.button(
            icon("x", size=16),
            on_click=lambda: EventsState.remove_recipient(email),
            type="button",
            aria_label=f"Remove {email}",
            style={"display": "flex", "cursor": "pointer", "background": "none", "border": "none", "padding": "0"},
        ),
        class_name="m3-status-chip",
        custom_attrs={"data-status": "recipient"},
        style={"height": "32px", "gap": "6px", "padding": "0 8px 0 12px"},
    )


def _recipients_editor() -> rx.Component:
    """Paste-or-upload recipient management."""
    return rx.vstack(
        rx.hstack(
            icon("group", size=18, color="var(--md-sys-color-on-surface-variant)"),
            rx.text("Recipients", font="var(--md-sys-typescale-body-small)"),
            rx.text("*", color="var(--md-sys-color-error)"),
            rx.spacer(),
            rx.cond(
                EventsState.recipients.length() > 0,
                rx.button(
                    f"Clear all ({EventsState.recipients.length()})",
                    on_click=EventsState.clear_recipients,
                    type="button",
                    variant="ghost",
                    size="1",
                ),
            ),
            align="center",
            spacing="2",
            width="100%",
        ),
        rx.hstack(
            rx.input(
                placeholder="name@example.com, another@example.com",
                value=EventsState.recipient_draft,
                on_change=EventsState.set_recipient_draft,
                size="3",
                width="100%",
            ),
            rx.button(
                "Add",
                on_click=EventsState.add_recipients,
                type="button",
                variant="soft",
                size="3",
            ),
            spacing="2",
            width="100%",
        ),
        rx.upload(
            rx.hstack(
                icon("upload_file", size=18),
                rx.text("Drop a CSV or TXT list, or click to browse", font="var(--md-sys-typescale-body-small)"),
                align="center",
                justify="center",
                spacing="2",
            ),
            id=UPLOAD_ID,
            accept={"text/csv": [".csv"], "text/plain": [".txt"]},
            multiple=False,
            on_drop=EventsState.upload_recipients(rx.upload_files(upload_id=UPLOAD_ID)),  # type: ignore[call-arg]
            border="1px dashed var(--md-sys-color-outline)",
            border_radius="var(--md-sys-shape-corner-medium)",
            padding="0.75rem",
            width="100%",
            cursor="pointer",
        ),
        rx.cond(
            EventsState.recipients_error != "",
            rx.text(
                EventsState.recipients_error,
                font="var(--md-sys-typescale-body-small)",
                color="var(--md-sys-color-error)",
            ),
        ),
        rx.flex(
            rx.foreach(EventsState.recipients, _recipient_chip),
            wrap="wrap",
            gap="0.5rem",
            width="100%",
        ),
        spacing="2",
        width="100%",
    )


def event_form_dialog() -> rx.Component:
    """The shared add/edit dialog."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.hstack(
                rx.flex(
                    icon("event", size=24, color="var(--md-sys-color-on-secondary-container)"),
                    background="var(--md-sys-color-secondary-container)",
                    border_radius="var(--md-sys-shape-corner-full)",
                    min_width="3rem",
                    height="3rem",
                    align="center",
                    justify="center",
                ),
                rx.vstack(
                    rx.dialog.title(
                        rx.cond(EventsState.is_editing, "Edit Event", "Add New Event"),
                        margin="0",
                    ),
                    rx.dialog.description(
                        "Welcome emails send 2 days before the start date, thank-you emails "
                        "2 days before the end date.",
                    ),
                    spacing="1",
                    align_items="start",
                ),
                spacing="4",
                margin_bottom="1.5em",
                align="center",
                width="100%",
            ),
            rx.form.root(
                rx.flex(
                    rx.flex(
                        form_field(
                            "Event ID",
                            "e.g. FALL-2026-01",
                            "text",
                            "event_id",
                            "tag",
                            required=True,
                            error_message=EventsState.id_error,
                            helper="Unique key. Cannot be changed after creation.",
                        ),
                        form_field(
                            "Event Name",
                            "e.g. Flag Football Program",
                            "text",
                            "event_name",
                            "event",
                            required=True,
                            error_message=EventsState.name_error,
                        ),
                        direction=rx.breakpoints(initial="column", sm="row"),
                        gap="1rem",
                        width="100%",
                    ),
                    rx.flex(
                        form_field("Start Date", "", "date", "start_date", "calendar-days", required=True),
                        form_field(
                            "End Date",
                            "",
                            "date",
                            "end_date",
                            "calendar-days",
                            required=True,
                            error_message=EventsState.date_error,
                        ),
                        direction=rx.breakpoints(initial="column", sm="row"),
                        gap="1rem",
                        width="100%",
                    ),
                    rx.flex(
                        form_field("Start Time", "5:20 PM", "text", "start_time", "clock"),
                        form_field("End Time", "6:10 PM", "text", "end_time", "clock"),
                        direction=rx.breakpoints(initial="column", sm="row"),
                        gap="1rem",
                        width="100%",
                    ),
                    form_field("Location", "Covert Avenue School", "text", "location_name", "location_on"),
                    form_field("Address", "14 Covert Ave, Elmont, NY 11003", "text", "location_address", "map"),
                    rx.flex(
                        form_field("Contact Phone", "(516) 450-8343", "text", "contact_phone", "call"),
                        form_field("Contact Email", "info@example.com", "email", "contact_email", "mail"),
                        direction=rx.breakpoints(initial="column", sm="row"),
                        gap="1rem",
                        width="100%",
                    ),
                    form_field(
                        "Event Details",
                        "Context the email writer should know — audience, what to bring, tone.",
                        "text",
                        "event_details",
                        "notebook-pen",
                        helper="Used when generating email copy.",
                    ),
                    rx.divider(margin_y="0.5rem", color="var(--md-sys-color-outline-variant)"),
                    _recipients_editor(),
                    direction="column",
                    spacing="3",
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button("Cancel", variant="ghost", color_scheme="gray", type="button"),
                    ),
                    rx.form.submit(
                        rx.button(
                            rx.cond(EventsState.is_editing, "Save Changes", "Create Event"),
                            variant="ghost",
                        ),
                        as_child=True,
                    ),
                    padding_top="1.5em",
                    spacing="2",
                    justify="end",
                ),
                on_submit=EventsState.submit_event,
                reset_on_submit=False,
            ),
            max_width="720px",
        ),
        open=EventsState.dialog_open,
        on_open_change=lambda is_open: rx.cond(
            is_open,
            EventsState.open_add_dialog(),
            EventsState.close_dialog(),
        ),
    )


def add_event_button() -> rx.Component:
    return rx.button(
        icon("plus", size=20),
        rx.text("Add Event", display=["none", "none", "block"]),
        on_click=EventsState.open_add_dialog,
        size="3",
        variant="solid",
    )


def edit_event_button(event: Event) -> rx.Component:
    return rx.tooltip(
        rx.icon_button(
            icon("square-pen", size=20),
            on_click=lambda: EventsState.open_edit_dialog(event),
            size="2",
            variant="ghost",
            aria_label="Edit event",
        ),
        content="Edit event",
    )


def cancel_event_button(event: Event) -> rx.Component:
    """Flag or clear cancellation, behind a confirmation for the destructive direction."""
    return rx.cond(
        event.cancellation_flag,
        rx.tooltip(
            rx.icon_button(
                icon("restore", size=20),
                on_click=lambda: EventsState.set_cancelled(event.event_id, False),
                size="2",
                variant="ghost",
                aria_label="Clear cancellation flag",
            ),
            content="Clear the cancellation flag",
        ),
        rx.alert_dialog.root(
            rx.alert_dialog.trigger(
                rx.icon_button(
                    icon("cancel", size=20),
                    size="2",
                    variant="ghost",
                    color_scheme="tomato",
                    aria_label="Mark event cancelled",
                ),
            ),
            rx.alert_dialog.content(
                rx.alert_dialog.title("Mark event as cancelled?"),
                rx.alert_dialog.description(
                    f"A cancellation email will be sent to {event.recipients.length()} recipient(s) "
                    "on the next ecas run. This does not send immediately."
                ),
                rx.flex(
                    rx.alert_dialog.cancel(
                        rx.button("Keep event", variant="ghost", color_scheme="gray"),
                    ),
                    rx.alert_dialog.action(
                        rx.button(
                            "Mark cancelled",
                            variant="ghost",
                            color_scheme="tomato",
                            on_click=lambda: EventsState.set_cancelled(event.event_id, True),
                        ),
                    ),
                    spacing="2",
                    margin_top="24px",
                    justify="end",
                ),
                style={"max_width": 450},
            ),
        ),
    )
