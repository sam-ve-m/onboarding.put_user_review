# Jormungandr - Onboarding
from func.src.domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    InvalidOnboardingCurrentStep,
)
from func.src.services.user_review import UserReviewDataService
from tests.src.services.user_review.stubs import stub_unique_id

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.find_one_by_unique_id",
    return_value={"data": True},
)
async def test_when_get_user_successfully_then_return_user_data(mock_repository):
    user_data = await UserReviewDataService._get_user_data(unique_id=stub_unique_id)

    assert isinstance(user_data, dict)
    assert user_data.get("data") is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.find_one_by_unique_id",
    return_value=None,
)
async def test_when_not_found_an_user_then_raises(mock_repository):
    with pytest.raises(UserUniqueIdNotExists):
        await UserReviewDataService._get_user_data(unique_id=stub_unique_id)


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.OnboardingSteps.get_user_current_step",
    return_value="data_validation",
)
async def test_when_current_step_correct_then_return_true(mock_onboarding_steps):
    result = await UserReviewDataService.validate_current_onboarding_step(jwt="123")

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.OnboardingSteps.get_user_current_step",
    return_value="finished",
)
async def test_when_current_step_invalid_then_return_raises(mock_onboarding_steps):
    with pytest.raises(InvalidOnboardingCurrentStep):
        await UserReviewDataService.validate_current_onboarding_step(jwt="123")
