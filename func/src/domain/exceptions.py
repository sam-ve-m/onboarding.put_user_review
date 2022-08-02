class ErrorOnDecodeJwt(Exception):
    msg = "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique id," \
          " jwt not decoded successfully"


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::get_registration_data::Not exists an user_data with this unique_id"


class InvalidEmail(Exception):
    msg = "Invalid email address"


class InternalServerError(Exception):
    pass
