import json
from typing import Any

import aiohttp
import httpx
from multidict import CIMultiDict, CIMultiDictProxy
from yarl import URL


def make_mock_handler(
    expected_method: str,
    expected_url: str,
    response_data: dict | list | None,
    status_code: int = httpx.codes.OK,
    expected_json: Any | None = None,
):
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == expected_method
        assert str(request.url) == expected_url
        if expected_json is not None:
            actual = json.loads(request.content.decode("utf-8"))
            assert actual == expected_json, f"Expected {expected_json}, got {actual}"
        return httpx.Response(status_code, json=response_data)

    return handler


class MockAsyncSession:
    """Minimal stand-in for aiohttp.ClientSession.

    Covers exactly the shape api_routes uses -- `async with session.post(...) as
    response: response.raise_for_status()`. Recorded calls are exposed so tests
    can assert the request was actually made, not just that nothing raised.
    """

    def __init__(self, status: int = 200):
        self.status = status
        self.calls: list[tuple[str, Any]] = []

    def post(self, url: str, json: Any | None = None):
        self.calls.append((url, json))
        return _MockAsyncResponse(self.status, url)


class _MockAsyncResponse:
    def __init__(self, status: int, url: str):
        self.status = status
        self.url = url

    def raise_for_status(self) -> None:
        if self.status >= 400:
            request_info = aiohttp.RequestInfo(
                url=URL(self.url),
                method="POST",
                headers=CIMultiDictProxy(CIMultiDict()),
                real_url=URL(self.url),
            )
            raise aiohttp.ClientResponseError(
                request_info=request_info,
                history=(),
                status=self.status,
                message=f"HTTP {self.status}",
            )

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc) -> bool:
        return False
