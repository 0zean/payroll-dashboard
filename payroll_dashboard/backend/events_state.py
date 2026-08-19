"""State for the events page."""

from datetime import date

import reflex as rx

from ..backend.event_api import cancel_event, create_event, fetch_events, update_event
from ..backend.recipients import parse_recipients
from ..backend.schemas import Event, EventEntry


class EventsState(rx.State):
    """Events loaded from the ecas sheet, plus the add/edit form."""

    events: list[Event] = []
    loading: bool = False
    search_value: str = ""

    # Dialog
    dialog_open: bool = False
    editing_event_id: str | None = None
    recipients: list[str] = []
    recipient_draft: str = ""

    # Validation
    id_error: str = ""
    name_error: str = ""
    date_error: str = ""
    recipients_error: str = ""

    @rx.var(cache=True)
    def filtered_events(self) -> list[Event]:
        """Events matching the search box, by name or location."""
        term = self.search_value.strip().lower()
        if not term:
            return self.events
        return [e for e in self.events if term in e.event_name.lower() or term in e.location_name.lower()]

    @rx.var(cache=True)
    def is_editing(self) -> bool:
        return self.editing_event_id is not None

    # Explicit setters: state_auto_setters is a no-op in Reflex 0.9.8.
    @rx.event
    def set_search_value(self, value: str) -> None:
        self.search_value = value

    @rx.event
    def set_recipient_draft(self, value: str) -> None:
        self.recipient_draft = value

    @rx.event
    def load_events(self) -> None:
        """Reload every event from the API."""
        self.loading = True
        try:
            self.events = fetch_events()
        finally:
            self.loading = False

    # Dialog
    def _clear_errors(self) -> None:
        self.id_error = ""
        self.name_error = ""
        self.date_error = ""
        self.recipients_error = ""

    @rx.event
    def open_add_dialog(self) -> None:
        """Open a blank create form."""
        self._clear_errors()
        self.editing_event_id = None
        self.recipients = []
        self.recipient_draft = ""
        self.dialog_open = True

    @rx.event
    def open_edit_dialog(self, event: Event) -> None:
        """Open the form pre-filled with *event*."""
        self._clear_errors()
        self.editing_event_id = event.event_id
        self.recipients = list(event.recipients)
        self.recipient_draft = ""
        self.dialog_open = True

    @rx.event
    def close_dialog(self) -> None:
        self._clear_errors()
        self.dialog_open = False
        self.editing_event_id = None

    # Recipients
    def ingest_recipient_text(self, raw: str) -> int:
        """Merge addresses parsed from *raw* into the list. Returns how many were new."""
        existing = {r.lower() for r in self.recipients}
        added = [r for r in parse_recipients(raw) if r.lower() not in existing]
        self.recipients = [*self.recipients, *added]
        return len(added)

    @rx.event
    def add_recipients(self) -> None:
        """Add whatever is typed in the draft box."""
        self.recipients_error = ""
        if self.ingest_recipient_text(self.recipient_draft):
            self.recipient_draft = ""
        else:
            self.recipients_error = "No valid email addresses found"

    @rx.event
    def remove_recipient(self, email: str) -> None:
        self.recipients = [r for r in self.recipients if r != email]

    @rx.event
    def clear_recipients(self) -> None:
        self.recipients = []

    @rx.event
    async def upload_recipients(self, files: list[rx.UploadFile]):
        """Merge a uploaded CSV/TXT list into the recipients."""
        added = 0
        for file in files:
            content = await file.read()
            added += self.ingest_recipient_text(content.decode("utf-8", errors="ignore"))

        if not added:
            self.recipients_error = "No valid email addresses found in that file"
            return rx.toast.warning("No new addresses found in that file", position="top-center")

        self.recipients_error = ""
        return rx.toast.success(f"Added {added} recipient(s)", position="top-center")

    # Submit
    def _validate(self, form_data: dict) -> bool:
        """Populate the *_error fields. Returns True when the form is submittable."""
        self._clear_errors()

        if not str(form_data.get("event_id", "")).strip():
            self.id_error = "Event ID is required"
        if not str(form_data.get("event_name", "")).strip():
            self.name_error = "Event name is required"

        start_raw = str(form_data.get("start_date", "")).strip()
        end_raw = str(form_data.get("end_date", "")).strip()
        if not start_raw or not end_raw:
            self.date_error = "Start and end dates are required"
        else:
            try:
                # A one-day event has start == end, so only an inversion is invalid.
                if date.fromisoformat(end_raw) < date.fromisoformat(start_raw):
                    self.date_error = "End date cannot be before the start date"
            except ValueError:
                self.date_error = "Dates must be valid calendar dates"

        if not self.recipients:
            self.recipients_error = "Add at least one recipient"

        return not any((self.id_error, self.name_error, self.date_error, self.recipients_error))

    @rx.event
    def submit_event(self, form_data: dict):
        """Create or update an event, depending on whether the form is in edit mode."""
        if not self._validate(form_data):
            self.dialog_open = True
            return None

        entry = EventEntry(
            event_id=str(form_data.get("event_id", "")).strip(),
            event_name=str(form_data.get("event_name", "")).strip(),
            start_date=str(form_data.get("start_date", "")).strip(),
            end_date=str(form_data.get("end_date", "")).strip(),
            start_time=str(form_data.get("start_time", "")).strip(),
            end_time=str(form_data.get("end_time", "")).strip(),
            location_name=str(form_data.get("location_name", "")).strip(),
            location_address=str(form_data.get("location_address", "")).strip(),
            recipients=list(self.recipients),
            contact_phone=str(form_data.get("contact_phone", "")).strip(),
            contact_email=str(form_data.get("contact_email", "")).strip(),
            event_details=str(form_data.get("event_details", "")).strip(),
        )

        try:
            if self.editing_event_id:
                update_event(self.editing_event_id, entry)
                message = "Event updated"
            else:
                create_event(entry)
                message = "Event created"
        except Exception as e:
            # Surfaced to the user as a toast rather than failing the page.
            return rx.toast.error(f"Could not save event: {e}", position="top-center")

        self.events = fetch_events()
        self.dialog_open = False
        self.editing_event_id = None
        return rx.toast.success(f"{message} 🎉", position="top-center")

    # Cancellation
    @rx.event
    def set_cancelled(self, event_id: str, cancelled: bool):
        """Flag or unflag an event for cancellation.

        ecas sends the email on its next run, so the toast says queued, not sent.
        """
        try:
            cancel_event(event_id, cancelled=cancelled)
        except Exception as e:
            # Surfaced to the user as a toast rather than failing the page.
            return rx.toast.error(f"Could not update event: {e}", position="top-center")

        self.events = fetch_events()
        message = "Cancellation queued for the next ecas run" if cancelled else "Cancellation flag cleared"
        return rx.toast.success(message, position="top-center")
