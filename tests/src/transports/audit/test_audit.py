from datetime import datetime

from func.src.domain.exceptions.exceptions import ErrorOnSendAuditLog
from func.src.transports.audit.transport import Audit
from tests.src.services.user_review.stubs import stub_user_review_model
from regis import RegisResponse, RiskRatings, RiskValidations
from unittest.mock import patch

import pytest


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(1, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_success_to_record_message_then_return_true(
    mock_config, mock_persephone
):
    result = await Audit.record_message_log_to_update_registration_data(
        user_review_model=stub_user_review_model
    )

    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(0, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_when_fail_to_record_message_then_raises(mock_config, mock_persephone):
    with pytest.raises(ErrorOnSendAuditLog):
        await Audit.record_message_log_to_update_registration_data(
            user_review_model=stub_user_review_model
        )


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(1, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_record_message_log_to_rate_client_risk_when_success(
    mock_config, mock_persephone
):
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
    stub_user_review_model.add_risk_data(risk_data=risk_data_stub)
    result = await Audit.record_message_log_to_rate_client_risk(
        user_review_model=stub_user_review_model
    )
    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.transports.audit.transport.Persephone.send_to_persephone",
    return_value=(0, 0),
)
@patch("func.src.transports.audit.transport.config")
async def test_record_message_log_to_rate_client_risk_when_failed(
    mock_config, mock_persephone
):
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
    stub_user_review_model.add_risk_data(risk_data=risk_data_stub)
    with pytest.raises(ErrorOnSendAuditLog):
        await Audit.record_message_log_to_rate_client_risk(
            user_review_model=stub_user_review_model
        )
