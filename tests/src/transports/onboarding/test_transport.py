from func.src.domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk
from func.src.transports.onboarding_steps.transport import OnboardingSteps, Onboarding
from tests.src.transports.onboarding.stubs import (
    stub_request_success,
    stub_request_failure,
)

from unittest.mock import patch

import pytest


@pytest.mark.asyncio
@patch("func.src.transports.onboarding_steps.transport.config")
@patch(
    "func.src.transports.onboarding_steps.transport.AsyncClient.get",
    return_value=stub_request_success,
)
async def test_when_success_to_get_onboarding_steps_then_returns_current_step(
    mock_httpx_client, mock_config
):
    user_current_step = await OnboardingSteps.get_user_current_step(jwt="12345")
    assert isinstance(user_current_step, Onboarding)
    assert user_current_step.step == "selfie"
    assert user_current_step.anti_fraud == "approved"


@pytest.mark.asyncio
@patch("func.src.transports.onboarding_steps.transport.config")
@patch(
    "func.src.transports.onboarding_steps.transport.AsyncClient.get",
    return_value=stub_request_failure,
)
async def test_when_failure_to_get_onboarding_steps_then_raises(
    mock_httpx_client, mock_config
):
    with pytest.raises(OnboardingStepsStatusCodeNotOk):
        await OnboardingSteps.get_user_current_step(jwt="12345")
