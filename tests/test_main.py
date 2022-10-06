# PROJECT IMPORTS
import logging.config
from http import HTTPStatus
from unittest.mock import patch, MagicMock

import flask
import pytest
from decouple import RepositoryEnv, Config

from src.domain.user_review.validator import UserReviewData
from src.services.user_enumerate_data import UserEnumerateService

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from main import update_user_review_data
                from src.services.jwt import JwtService
                from src.domain.enums.code import InternalCode
                from src.domain.response.model import ResponseModel
                from src.domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk, \
                    InvalidOnboardingCurrentStep, \
                    ErrorOnGetUniqueId, \
                    UserUniqueIdNotExists, InvalidNationality, HighRiskActivityNotAllowed, ErrorOnSendAuditLog, \
                    ErrorOnUpdateUser, \
                    ErrorOnDecodeJwt
                from src.services.user_review import UserReviewDataService

error_on_decode_jwt_case = (
    ErrorOnDecodeJwt(),
    ErrorOnDecodeJwt.msg,
    InternalCode.JWT_INVALID,
    "Error when trying to decode jwt",
    HTTPStatus.UNAUTHORIZED
)
onboarding_steps_status_code_not_ok_case = (
    OnboardingStepsStatusCodeNotOk(),
    OnboardingStepsStatusCodeNotOk.msg,
    InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
invalid_onboarding_current_step_case = (
    InvalidOnboardingCurrentStep(),
    InvalidOnboardingCurrentStep.msg.format(""),
    InternalCode.ONBOARDING_STEP_INCORRECT,
    "User is not in correct step",
    HTTPStatus.BAD_REQUEST
)
error_on_get_unique_id_case = (
    ErrorOnGetUniqueId(),
    ErrorOnGetUniqueId.msg,
    InternalCode.JWT_INVALID,
    "Fail to get unique_id",
    HTTPStatus.UNAUTHORIZED
)
user_unique_id_not_exists_case = (
    UserUniqueIdNotExists(),
    UserUniqueIdNotExists.msg,
    InternalCode.DATA_NOT_FOUND,
    "There is no user with this unique_id",
    HTTPStatus.BAD_REQUEST
)
invalid_nationality_case = (
    InvalidNationality(),
    InvalidNationality.msg,
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST
)
high_risk_activity_not_allowed_case = (
    HighRiskActivityNotAllowed(),
    HighRiskActivityNotAllowed.msg,
    InternalCode.INVALID_PARAMS,
    "High risk occupation not allowed",
    HTTPStatus.FORBIDDEN
)
error_on_send_audit_log_case = (
    ErrorOnSendAuditLog(),
    ErrorOnSendAuditLog.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
error_on_update_user_case = (
    ErrorOnUpdateUser(),
    ErrorOnUpdateUser.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
value_error_case = (
    ValueError("dummy"),
    "dummy",
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR
)


@pytest.mark.asyncio
@pytest.mark.parametrize("exception,error_message,internal_status_code,response_message,response_status_code", [
    error_on_decode_jwt_case,
    onboarding_steps_status_code_not_ok_case,
    invalid_onboarding_current_step_case,
    error_on_get_unique_id_case,
    user_unique_id_not_exists_case,
    invalid_nationality_case,
    high_risk_activity_not_allowed_case,
    error_on_send_audit_log_case,
    error_on_update_user_case,
    value_error_case,
    exception_case,
])
@patch.object(UserReviewDataService, "validate_current_onboarding_step")
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(UserReviewData, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_update_user_review_data_raising_errors(
        mocked_build_response, mocked_response_instance, mocked_model,
        mocked_jwt_decode, mocked_logger, mocked_service, monkeypatch,
        exception, error_message, internal_status_code, response_message, response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_jwt_decode.side_effect = exception
    await update_user_review_data()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False,
        code=internal_status_code,
        message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(UserReviewDataService, "validate_current_onboarding_step")
@patch.object(Gladsheim, "error")
@patch.object(JwtService, "decode_jwt_and_get_unique_id")
@patch.object(UserReviewDataService, "validate_current_onboarding_step")
@patch.object(UserEnumerateService, "__init__", return_value=None)
@patch.object(UserEnumerateService, "validate_enumerate_params")
@patch.object(UserReviewDataService, "apply_rules_to_update_user_review")
@patch.object(UserReviewData, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_update_user_review_data(
        mocked_build_response, mocked_response_instance, mocked_model,
        mocked_rules_application, mocked_validation_server_instance, mocked_instance,
        mocked_validation, mocked_jwt_decode, mocked_logger, mocked_service, monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await update_user_review_data()
    mocked_jwt_decode.assert_called()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=True,
        code=InternalCode.SUCCESS,
        message="User review data successfully validated",
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
