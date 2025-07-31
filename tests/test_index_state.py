from unittest import mock

import pytest

from payroll_dashboard.backend.index_state import IndexState


@pytest.mark.asyncio
async def test_start_download_sets_loading():
    state = IndexState()
    gen = state.start_download()
    await gen.__anext__()
    assert state.download_loading is True


@pytest.mark.asyncio
async def test_finish_download_success(monkeypatch):
    state = IndexState()
    monkeypatch.setattr("payroll_dashboard.backend.index_state.url_base", "/test/")
    
    class MockResponse:
        status_code = 200
        content = b"fake_excel_data"

    monkeypatch.setattr("payroll_dashboard.backend.index_state.requests.get", lambda url: MockResponse())
    
    result = []
    async for x in state.finish_download():
        result.append(x)
    assert state.download_loading is False
    assert any("Downloaded payroll!" in str(r) for r in result)


@pytest.mark.asyncio
async def test_finish_download_error(monkeypatch):
    state = IndexState()
    monkeypatch.setattr("payroll_dashboard.backend.index_state.url_base", "/test/")
    
    class MockResponse:
        status_code = 500
        content = b"fake_excel_data"

    monkeypatch.setattr("payroll_dashboard.backend.index_state.requests.get", lambda url: MockResponse())
    
    result = []
    async for x in state.finish_download():
        result.append(x)
    assert state.download_loading is False
    assert any("Error downloading payroll" in str(r) for r in result)


@pytest.mark.asyncio
async def test_start_clean_sets_loading():
    state = IndexState()
    gen = state.start_clean()
    await gen.__anext__()
    assert state.clear_loading is True


@pytest.mark.asyncio
async def test_finish_clean_success(monkeypatch):
    state = IndexState()
    monkeypatch.setattr("payroll_dashboard.backend.index_state.clear_payroll", mock.AsyncMock())
    result = []
    async for x in state.finish_clean():
        result.append(x)
    assert state.clear_loading is False
    assert any("Cleared payroll!" in str(r) for r in result)


@pytest.mark.asyncio
async def test_finish_clean_error(monkeypatch):
    state = IndexState()
    monkeypatch.setattr(
        "payroll_dashboard.backend.index_state.clear_payroll", mock.AsyncMock(side_effect=Exception("fail"))
    )
    result = []
    async for x in state.finish_clean():
        result.append(x)
    assert state.clear_loading is False
    assert any("Error clearing payroll" in str(r) for r in result)
