import json
from typing import Any

import httpx


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
