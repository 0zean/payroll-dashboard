"""Tests for the events API client."""

from unittest.mock import patch

import httpx

from payroll_dashboard.backend.event_api import (
    cancel_event,
    create_event,
    fetch_events,
    update_event,
)
from payroll_dashboard.backend.schemas import EventEntry
from tests.mock_utils import make_mock_handler

BASE = "http://127.0.0.1:8000/api"

EVENT_JSON = {
    "event_id": "E-1",
    "event_name": "Spring Clinic",
    "start_date": "2026-05-01",
    "end_date": "2026-05-03",
    "start_time": "9:00 AM",
    "end_time": "12:00 PM",
    "location_name": "Community Center",
    "location_address": "200 Main St",
    "recipients": ["c@x.com"],
    "platform": "direct",
    "contact_phone": "(516) 555-0199",
    "contact_email": "events@example.com",
    "event_details": "Bring water.",
    "cancellation_flag": False,
    "welcome_sent": True,
    "thank_you_sent": False,
    "cancellation_sent": False,
    "schedule": [
        {"email_type": "welcome", "trigger_date": "2026-04-29", "status": "sent", "sent": True},
        {"email_type": "thank_you", "trigger_date": "2026-05-01", "status": "scheduled", "sent": False},
        {"email_type": "cancellation", "trigger_date": None, "status": "inactive", "sent": False},
    ],
}


def _entry() -> EventEntry:
    return EventEntry(
        event_id="E-1",
        event_name="Spring Clinic",
        start_date="2026-05-01",
        end_date="2026-05-03",
        start_time="9:00 AM",
        end_time="12:00 PM",
        location_name="Community Center",
        location_address="200 Main St",
        recipients=["c@x.com"],
        contact_phone="(516) 555-0199",
        contact_email="events@example.com",
        event_details="Bring water.",
    )


def test_fetch_events_parses_response(mock_httpx_client):
    handler = make_mock_handler("GET", f"{BASE}/events", [EVENT_JSON])
    client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.event_api.get_client", return_value=client):
        events = fetch_events()

    assert len(events) == 1
    assert events[0].event_id == "E-1"
    assert events[0].recipients == ["c@x.com"]
    assert events[0].welcome_sent is True
    assert [s.status for s in events[0].schedule] == ["sent", "scheduled", "inactive"]


def test_fetch_events_returns_empty_list_on_transport_error(mock_httpx_client):
    """A dead API must not take the page down."""

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused")

    client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.event_api.get_client", return_value=client):
        assert fetch_events() == []


def test_create_event_posts_entry(mock_httpx_client):
    handler = make_mock_handler(
        "POST",
        f"{BASE}/events",
        EVENT_JSON,
        expected_json=_entry().model_dump(mode="json"),
    )
    client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.event_api.get_client", return_value=client):
        created = create_event(_entry())

    assert created.event_id == "E-1"


def test_update_event_puts_to_the_id_path(mock_httpx_client):
    handler = make_mock_handler(
        "PUT",
        f"{BASE}/events/E-1",
        EVENT_JSON,
        expected_json=_entry().model_dump(mode="json"),
    )
    client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.event_api.get_client", return_value=client):
        assert update_event("E-1", _entry()).event_id == "E-1"


def test_cancel_event_posts_to_the_cancel_path(mock_httpx_client):
    handler = make_mock_handler("POST", f"{BASE}/events/E-1/cancel?cancelled=true", EVENT_JSON)
    client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.event_api.get_client", return_value=client):
        assert cancel_event("E-1", cancelled=True).event_id == "E-1"


def test_uncancel_event_passes_false(mock_httpx_client):
    handler = make_mock_handler("POST", f"{BASE}/events/E-1/cancel?cancelled=false", EVENT_JSON)
    client = mock_httpx_client(handler)

    with patch("payroll_dashboard.backend.event_api.get_client", return_value=client):
        cancel_event("E-1", cancelled=False)
