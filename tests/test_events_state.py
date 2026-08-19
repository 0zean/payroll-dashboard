"""Tests for EventsState -- the events page's state machine."""

from unittest.mock import patch

import pytest

from payroll_dashboard.backend.events_state import EventsState
from payroll_dashboard.backend.schemas import EmailSchedule, Event


@pytest.fixture
def events_state():
    return EventsState()


def _event(event_id: str = "E-1", **overrides) -> Event:
    event = Event(
        event_id=event_id,
        event_name="Spring Clinic",
        start_date="2026-05-01",
        end_date="2026-05-03",
        recipients=["c@x.com"],
        schedule=[EmailSchedule(email_type="welcome", trigger_date="2026-04-29", status="scheduled", sent=False)],
    )
    return event.model_copy(update=overrides)


FORM = {
    "event_id": "E-1",
    "event_name": "Spring Clinic",
    "start_date": "2026-05-01",
    "end_date": "2026-05-03",
    "start_time": "9:00 AM",
    "end_time": "12:00 PM",
    "location_name": "Community Center",
    "location_address": "200 Main St",
    "contact_phone": "(516) 555-0199",
    "contact_email": "events@example.com",
    "event_details": "Bring water.",
}


# Loading
def test_load_events_populates_state(events_state):
    with patch("payroll_dashboard.backend.events_state.fetch_events", return_value=[_event("A"), _event("B")]):
        events_state.load_events()

    assert [e.event_id for e in events_state.events] == ["A", "B"]
    assert events_state.loading is False


def test_load_events_survives_an_empty_sheet(events_state):
    with patch("payroll_dashboard.backend.events_state.fetch_events", return_value=[]):
        events_state.load_events()

    assert events_state.events == []


# Filtering
def test_filtered_events_matches_name_case_insensitively(events_state):
    events_state.events = [_event("A", event_name="Flag Football"), _event("B", event_name="Chess Club")]
    events_state.search_value = "flag"

    assert [e.event_id for e in events_state.filtered_events] == ["A"]


def test_filtered_events_matches_location(events_state):
    events_state.events = [
        _event("A", location_name="Covert Avenue School"),
        _event("B", location_name="Community Center"),
    ]
    events_state.search_value = "covert"

    assert [e.event_id for e in events_state.filtered_events] == ["A"]


def test_filtered_events_returns_everything_when_search_is_blank(events_state):
    events_state.events = [_event("A"), _event("B")]
    events_state.search_value = "   "

    assert len(events_state.filtered_events) == 2


# Validation
def test_submit_rejects_a_blank_event_name(events_state):
    events_state.submit_event({**FORM, "event_name": "  "})

    assert events_state.name_error
    assert events_state.dialog_open is True  # stays open so the user can fix it


def test_submit_rejects_end_before_start(events_state):
    events_state.submit_event({**FORM, "start_date": "2026-05-10", "end_date": "2026-05-01"})

    assert events_state.date_error


def test_submit_rejects_a_blank_event_id(events_state):
    events_state.submit_event({**FORM, "event_id": ""})

    assert events_state.id_error


def test_submit_accepts_a_single_day_event(events_state):
    events_state.recipients = ["a@x.com"]
    with patch("payroll_dashboard.backend.events_state.create_event", return_value=_event()) as created:
        events_state.submit_event({**FORM, "start_date": "2026-05-01", "end_date": "2026-05-01"})

    assert created.called
    assert not events_state.date_error


# Create / update
def test_submit_creates_when_not_editing(events_state):
    events_state.recipients = ["a@x.com"]

    with patch("payroll_dashboard.backend.events_state.create_event", return_value=_event()) as created:
        with patch("payroll_dashboard.backend.events_state.fetch_events", return_value=[_event()]):
            events_state.submit_event(FORM)

    entry = created.call_args[0][0]
    assert entry.event_id == "E-1"
    assert entry.recipients == ["a@x.com"]
    assert events_state.dialog_open is False


def test_submit_updates_when_editing(events_state):
    events_state.editing_event_id = "E-1"
    events_state.recipients = ["a@x.com"]

    with patch("payroll_dashboard.backend.events_state.update_event", return_value=_event()) as updated:
        with patch("payroll_dashboard.backend.events_state.fetch_events", return_value=[_event()]):
            events_state.submit_event({**FORM, "event_name": "Renamed"})

    assert updated.call_args[0][0] == "E-1"
    assert updated.call_args[0][1].event_name == "Renamed"


def test_open_edit_dialog_loads_the_event_into_the_form(events_state):
    event = _event(event_details="Ages 5-10", recipients=["x@y.com", "z@y.com"])
    events_state.events = [event]

    events_state.open_edit_dialog(event)

    assert events_state.editing_event_id == "E-1"
    assert events_state.recipients == ["x@y.com", "z@y.com"]
    assert events_state.dialog_open is True


def test_open_add_dialog_clears_a_previous_edit(events_state):
    events_state.editing_event_id = "E-9"
    events_state.recipients = ["stale@x.com"]

    events_state.open_add_dialog()

    assert events_state.editing_event_id is None
    assert events_state.recipients == []


# Recipients
def test_add_recipients_appends_and_clears_the_draft(events_state):
    events_state.recipient_draft = "a@x.com, b@x.com"

    events_state.add_recipients()

    assert events_state.recipients == ["a@x.com", "b@x.com"]
    assert events_state.recipient_draft == ""


def test_add_recipients_dedupes_against_existing(events_state):
    events_state.recipients = ["a@x.com"]
    events_state.recipient_draft = "A@X.COM, b@x.com"

    events_state.add_recipients()

    assert events_state.recipients == ["a@x.com", "b@x.com"]


def test_add_recipients_reports_when_nothing_parsed(events_state):
    events_state.recipient_draft = "not-an-email"

    events_state.add_recipients()

    assert events_state.recipients == []
    assert events_state.recipients_error


def test_remove_recipient(events_state):
    events_state.recipients = ["a@x.com", "b@x.com"]

    events_state.remove_recipient("a@x.com")

    assert events_state.recipients == ["b@x.com"]


def test_clear_recipients(events_state):
    events_state.recipients = ["a@x.com", "b@x.com"]

    events_state.clear_recipients()

    assert events_state.recipients == []


def test_ingest_uploaded_list_appends_without_losing_existing(events_state):
    """Uploading a list adds to what is there; clearing is a separate explicit action."""
    events_state.recipients = ["keep@x.com"]

    events_state.ingest_recipient_text("name,email\nAlice,a@x.com\nBob,b@x.com")

    assert events_state.recipients == ["keep@x.com", "a@x.com", "b@x.com"]


# Cancellation
def test_set_cancelled_calls_the_api_and_reloads(events_state):
    with patch("payroll_dashboard.backend.events_state.cancel_event", return_value=_event()) as cancelled:
        with patch(
            "payroll_dashboard.backend.events_state.fetch_events",
            return_value=[_event(cancellation_flag=True)],
        ):
            events_state.set_cancelled("E-1", True)

    assert cancelled.call_args[0][0] == "E-1"
    assert cancelled.call_args[1]["cancelled"] is True
    assert events_state.events[0].cancellation_flag is True
