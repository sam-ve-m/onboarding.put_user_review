# Jormungandr - Onboarding
from func.src.domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    InvalidOnboardingCurrentStep,
    ErrorToUpdateUser,
)
from func.src.services.user_review import UserReviewDataService
from tests.src.services.user_review.stubs import (
    stub_unique_id,
    stub_payload_validated,
    stub_user_from_database,
    stub_user_updated,
    stub_user_not_updated,
    stub_new_registration_data,
)

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


@pytest.mark.asyncio
@patch("func.src.services.user_review.IaraClient.send_to_sinacor_registration_queue")
@patch("func.src.services.user_review.UserReviewDataService._update_user_review")
@patch("func.src.services.user_review.Audit.record_message_log")
@patch(
    "func.src.services.user_review.UserReviewDataService._get_user_data",
    return_value=stub_user_from_database,
)
async def test_when_apply_rules_successfully_then_return_true(
    mock_get_user, mock_audit, mock_update, mock_iara
):
    result = await UserReviewDataService.apply_rules_to_update_user_review(
        unique_id=stub_unique_id, payload_validated=stub_payload_validated
    )

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_one_with_user_review_data",
    return_value=stub_user_updated,
)
async def test_when_update_user_successfully_then_return_true(mock_update_user):
    result = await UserReviewDataService._update_user_review(
        unique_id=stub_unique_id, new_user_registration_data={}
    )

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_one_with_user_review_data",
    return_value=stub_user_not_updated,
)
async def test_when_failure_to_update_user_then_raises(mock_update_user):
    with pytest.raises(ErrorToUpdateUser):
        await UserReviewDataService._update_user_review(
            unique_id=stub_unique_id, new_user_registration_data={}
        )
