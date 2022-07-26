# Jormungandr - Onboarding
from src.domain.response.model import ResponseModel
from src.domain.enums.code import InternalCode
from src.domain.exceptions import ErrorOnDecodeJwt, UserUniqueIdNotExists
from src.services.jwt import JwtService
from src.services.user_review import UserReviewDataService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response


async def update_user_data() -> Response:
    jwt = request.headers.get("x-thebes-answer")
    try:
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        result = await UserReviewDataService.get_registration_data(unique_id=unique_id)
        response = ResponseModel(
            result=result,
            success=True,
            code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="Error when trying to decode jwt"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=True, code=InternalCode.DATA_NOT_FOUND, message="There is no user_data with this token"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message="Unexpected error occurred"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
