from datetime import datetime
from unittest.mock import patch, AsyncMock

import pytest
from regis import Regis, RegisResponse, RiskRatings, RiskValidations

from func.src.domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    InvalidOnboardingCurrentStep,
    ErrorToUpdateUser,
    CriticalRiskClientNotAllowed,
    FailedToGetData,
    InvalidOnboardingAntiFraud,
)
from func.src.domain.user_review.model import UserReviewModel
from func.src.services.user_review import UserReviewDataService
from func.src.domain.models.onboarding import Onboarding
from tests.src.services.user_review.stubs import (
    stub_unique_id,
    stub_payload_validated,
    stub_user_from_database,
    stub_user_updated,
    stub_user_not_updated,
    stub_user_review_model,
    stub_device_info,
)


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
@patch("func.src.services.user_review.OnboardingSteps.get_user_current_step")
async def test_validate_current_onboarding_step_when_step_is_ok(mock_onboarding_steps):
    step_return_dummy = Onboarding("data_validation", "approved")
    mock_onboarding_steps.return_value = step_return_dummy
    result = await UserReviewDataService.validate_current_onboarding_step(jwt="123")
    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.OnboardingSteps.get_user_current_step",
)
async def test_validate_current_onboarding_step_when_current_step_is_wrong(
    mock_onboarding_steps,
):
    step_return_dummy = Onboarding("finished", "approved")
    mock_onboarding_steps.return_value = step_return_dummy
    with pytest.raises(InvalidOnboardingCurrentStep):
        await UserReviewDataService.validate_current_onboarding_step(jwt="123")


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.OnboardingSteps.get_user_current_step",
)
async def test_validate_current_onboarding_step_when_anti_fraud_is_not_approved(
    mock_onboarding_steps,
):
    step_return_dummy = Onboarding("data_validation", "reproved")
    mock_onboarding_steps.return_value = step_return_dummy
    with pytest.raises(InvalidOnboardingAntiFraud):
        await UserReviewDataService.validate_current_onboarding_step(jwt="123")


@pytest.mark.asyncio
@patch("func.src.services.user_review.UserReviewDataService.rate_client_risk")
@patch("func.src.services.user_review.IaraClient.send_to_sinacor_registration_queue")
@patch("func.src.services.user_review.UserReviewDataService._update_user_review")
@patch(
    "func.src.services.user_review.Audit.record_message_log_to_update_registration_data"
)
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch(
    "func.src.services.user_review.UserReviewDataService._get_user_data",
    return_value=stub_user_from_database,
)
@patch.object(UserReviewModel, "__new__")
async def test_when_apply_rules_successfully_then_return_true(
    mocked_model,
    mock_get_user,
    mock_audit_registration_data,
    mock_audit_pld,
    mock_update,
    mock_iara,
    rate_risk,
):
    mocked_model.return_value = AsyncMock()
    result = await UserReviewDataService.apply_rules_to_update_user_review(
        unique_id=stub_unique_id,
        payload_validated=stub_payload_validated.dict(),
    )
    assert mocked_model.mock_calls[0].kwargs["device_info"] is None
    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_one_with_user_review_data",
    return_value=stub_user_updated,
)
@patch.object(ErrorToUpdateUser, "__init__")
async def test_when_update_user_successfully_then_return_true(
    mock___init__, mock_update_user
):
    result = await UserReviewDataService._update_user_review(
        unique_id=stub_unique_id, new_user_registration_data={}
    )
    mock___init__.assert_not_called()
    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_one_with_user_review_data",
    return_value=stub_user_not_updated,
)
async def test_when_failure_to_update_user_review_then_raises(mock_update_user):
    with pytest.raises(ErrorToUpdateUser):
        await UserReviewDataService._update_user_review(
            unique_id=stub_unique_id, new_user_registration_data={}
        )


@pytest.mark.asyncio
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch.object(
    Regis,
    "rate_client_risk",
)
async def test_rate_client_risk(rate_client_risk, audit_log):
    risk_data_stub = RegisResponse(
        risk_score=1,
        risk_rating=RiskRatings.LOW_RISK,
        risk_approval=True,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    rate_client_risk.return_value = risk_data_stub
    result = await UserReviewDataService.rate_client_risk(stub_user_review_model)
    assert rate_client_risk.called


@pytest.mark.asyncio
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch.object(
    Regis,
    "rate_client_risk",
)
async def test_rate_client_risk_when_risk_is_not_aprroved(rate_client_risk, audit_log):

    risk_data_stub = RegisResponse(
        risk_score=19,
        risk_rating=RiskRatings.CRITICAL_RISK,
        risk_approval=False,
        expiration_date=datetime.now(),
        risk_validations=RiskValidations(
            has_big_patrymony=True,
            lives_in_frontier_city=True,
            has_risky_profession=True,
            is_pep=True,
            is_pep_related=True,
        ),
    )
    rate_client_risk.return_value = risk_data_stub
    with pytest.raises(CriticalRiskClientNotAllowed):
        result = await UserReviewDataService.rate_client_risk(stub_user_review_model)
    assert rate_client_risk.called


@pytest.mark.asyncio
@patch("func.src.services.user_review.Audit.record_message_log_to_rate_client_risk")
@patch.object(
    Regis,
    "rate_client_risk",
)
async def test_rate_client_risk_when_exception_happens(rate_client_risk, audit_log):
    rate_client_risk.side_effect = Exception()
    with pytest.raises(FailedToGetData):
        result = await UserReviewDataService.rate_client_risk(stub_user_review_model)
    assert rate_client_risk.called


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_user",
    return_value=stub_user_updated,
)
async def test__update_user(mock_update_user):
    result = await UserReviewDataService._update_user(
        unique_id=stub_unique_id, new_data={}
    )

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.update_user",
    return_value=stub_user_not_updated,
)
async def test_when_failure_to_update_user_then_raises(mock_update_user):
    with pytest.raises(ErrorToUpdateUser):
        await UserReviewDataService._update_user(unique_id=stub_unique_id, new_data={})
