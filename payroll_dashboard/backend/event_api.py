"""HTTP client for the events endpoints on the payroll API."""

import httpx

from ..backend.schemas import Event, EventEntry
from ..backend.utils import get_client

url_base = "http://127.0.0.1:8000/api/"


def fetch_events() -> list[Event]:
    """Fetch every event. Returns an empty list if the API is unreachable."""
    try:
        response = get_client().get(f"{url_base}events")
        response.raise_for_status()
        return [Event(**row) for row in response.json()]
    except httpx.RequestError as e:
        print(f"Error fetching events: {e}")
        return []


def create_event(entry: EventEntry) -> Event:
    """Create a new event."""
    response = get_client().post(f"{url_base}events", json=entry.model_dump(mode="json"))
    response.raise_for_status()
    return Event(**response.json())


def update_event(event_id: str, entry: EventEntry) -> Event:
    """Update an event's editable fields."""
    response = get_client().put(f"{url_base}events/{event_id}", json=entry.model_dump(mode="json"))
    response.raise_for_status()
    return Event(**response.json())


def cancel_event(event_id: str, *, cancelled: bool = True) -> Event:
    """Set or clear an event's cancellation flag.

    ecas sends the cancellation email on its next run, so this queues it.
    """
    response = get_client().post(
        f"{url_base}events/{event_id}/cancel",
        params={"cancelled": str(cancelled).lower()},
    )
    response.raise_for_status()
    return Event(**response.json())
