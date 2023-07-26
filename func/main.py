from http import HTTPStatus

import flask
from etria_logger import Gladsheim
from decouple import config

from func.src.domain.enums.code import InternalCode
from func.src.domain.exceptions.exceptions import (
    ErrorOnDecodeJwt,
    UserUniqueIdNotExists,
    ErrorOnSendAuditLog,
    ErrorToUpdateUser,
    InvalidNationality,
    InvalidCity,
    InvalidState,
    InvalidEmail,
    InvalidActivity,
    InvalidMaritalStatus,
    InvalidCountryAcronym,
    InvalidOnboardingCurrentStep,
    OnboardingStepsStatusCodeNotOk,
    ErrorOnGetUniqueId,
    HighRiskActivityNotAllowed,
    CriticalRiskClientNotAllowed,
    InvalidOnboardingAntiFraud,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
    FinancialCapacityNotValid, InvalidApiKey,
)
from func.src.domain.response.model import ResponseModel
from func.src.domain.user_review.validator import UserReviewData
from func.src.services.jwt import JwtService
from func.src.services.user_enumerate_data import UserEnumerateService
from func.src.services.user_review import UserReviewDataService
from func.src.transports.device_info.transport import DeviceSecurity


async def _update_user_review_data_legacy(jwt: str):
    encoded_device_info = flask.request.headers.get("x-device-info")
    raw_payload = flask.request.json

    payload_validated = UserReviewData(**raw_payload)
    unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
    device_info = await DeviceSecurity.get_device_info(encoded_device_info)

    await UserReviewDataService.validate_current_onboarding_step(jwt=jwt)
    await UserEnumerateService(
        payload_validated=payload_validated
    ).validate_enumerate_params()

    await UserReviewDataService.apply_rules_to_update_user_review(
        unique_id=unique_id,
        payload_validated=payload_validated.dict(),
        device_info=device_info,
    )


async def _append_user_risk_validation(api_key: str):
    if config("API_KEY") != api_key:
        raise InvalidApiKey()
    if not (unique_id := flask.request.headers.get("unique_id")):
        raise ValueError("Missing unique id")
    await UserReviewDataService.apply_rules_to_update_user_review(
        unique_id=unique_id,
        payload_validated={},
    )


async def update_user_review_data() -> flask.Response:
    msg_error = "Unexpected error occurred"
    try:
        if jwt := flask.request.headers.get("x-thebes-answer"):
            await _update_user_review_data_legacy(jwt)
        elif api_key := flask.request.headers.get("x-api-key"):
            await _append_user_risk_validation(api_key)
        else:
            raise ErrorOnDecodeJwt()

        response = ResponseModel(
            success=True,
            message="User review data successfully validated",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except InvalidApiKey as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Invalid Api Key",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Error when trying to decode jwt",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except OnboardingStepsStatusCodeNotOk as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_REQUEST_FAILURE,
            message=msg_error,
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except InvalidOnboardingCurrentStep as ex:
        Gladsheim.error(error=ex, message=ex.msg.format(str(ex)))
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT,
            message="User is not in correct step",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except InvalidOnboardingAntiFraud as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.ONBOARDING_STEP_INCORRECT,
            message="User not approved",
        ).build_http_response(status=HTTPStatus.FORBIDDEN)
        return response

    except ErrorOnGetUniqueId as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message="Fail to get unique_id",
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.DATA_NOT_FOUND,
            message="There is no user with this unique_id",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except (
        InvalidNationality,
        InvalidCity,
        InvalidState,
        InvalidEmail,
        InvalidActivity,
        InvalidMaritalStatus,
        InvalidCountryAcronym,
        FinancialCapacityNotValid
    ) as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except HighRiskActivityNotAllowed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="High risk occupation not allowed",
        ).build_http_response(status=HTTPStatus.FORBIDDEN)
        return response

    except CriticalRiskClientNotAllowed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Critical risk client not allowed",
        ).build_http_response(status=HTTPStatus.FORBIDDEN)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorToUpdateUser as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoRequestFailed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR.value,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS.value,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ValueError as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
