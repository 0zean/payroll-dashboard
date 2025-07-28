from unittest import mock

import pytest

from payroll_dashboard.backend.onboard_state import OnboardingState


@pytest.mark.asyncio
async def test_start_onboard_sets_loading(monkeypatch):
    state = OnboardingState()
    form_data = {"employee_name": "Test", "pay_rate": 10}
    gen = state.start_onboard(form_data)
    # Should set onboarding and loading True, then yield finish_onboard
    await gen.__anext__()
    assert state.onboarding.employee_name == "Test"
    assert state.loading is True


@pytest.mark.asyncio
async def test_finish_onboard_success(monkeypatch):
    state = OnboardingState()
    state.onboarding = mock.Mock()
    monkeypatch.setattr("payroll_dashboard.backend.onboard_state.onboard_employee", mock.AsyncMock())
    monkeypatch.setattr("payroll_dashboard.backend.onboard_state.TableState.set_employee_names", mock.Mock())
    result = []
    async for x in state.finish_onboard():
        result.append(x)
    assert state.loading is False
    assert any("Onboarding updated successfully" in str(r) for r in result)


@pytest.mark.asyncio
async def test_finish_onboard_error(monkeypatch):
    state = OnboardingState()
    state.onboarding = mock.Mock()
    monkeypatch.setattr(
        "payroll_dashboard.backend.onboard_state.onboard_employee", mock.AsyncMock(side_effect=Exception("fail"))
    )
    result = []
    async for x in state.finish_onboard():
        result.append(x)
    assert state.loading is False
    assert any("Error onboarding employee" in str(r) for r in result)
