import asyncio
import atexit

import aiohttp
import httpx
import reflex as rx

from ..backend.schemas import Employee, PayrollStats

_session: aiohttp.ClientSession | None = None
_client: httpx.Client | None = None


def get_client() -> httpx.Client:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.Client()
    return _client


@atexit.register
def close_client_on_exit():
    if _client and not _client.is_closed:
        _client.close()


async def get_session() -> aiohttp.ClientSession:
    global _session
    if _session is None or _session.closed:
        _session = aiohttp.ClientSession()
    return _session


@atexit.register
def close_session_on_exit():
    if _session and not _session.closed:
        asyncio.run(_session.close())


def calculate_stats(data: list[Employee]) -> PayrollStats:
    total_hours = sum(employee.hours_worked for employee in data)
    unique_employees = len(set(employee.employee_name for employee in data))

    return PayrollStats(total_entries=len(data), total_hours=total_hours, employees_count=unique_employees)


def header_cell(text: str, icon_tag: str) -> rx.Component:
    from ..components.icon import icon

    return rx.table.column_header_cell(
        rx.hstack(
            icon(icon_tag, size=18),
            rx.text(text),
            align="center",
            spacing="2",
        ),
    )
