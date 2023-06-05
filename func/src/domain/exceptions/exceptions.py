class InvalidApiKey(Exception):
    msg = "Jormungandr-Onboarding::Invalid x-api-key supplied"


class ErrorOnDecodeJwt(Exception):
    msg = (
        "Jormungandr-Onboarding::decode_jwt_and_get_unique_id::Fail when trying to get unique id,"
        " jwt not decoded successfully"
    )


class ErrorOnSendAuditLog(Exception):
    msg = (
        "Jormungandr-Onboarding::update_user_with_complementary_data::Error when trying to send log audit on "
        "Persephone"
    )


class FinancialCapacityNotValid(Exception):
    msg = "Jormungandr-Account::Insufficient financial capacity"


class ErrorOnSendIaraMessage(Exception):
    msg = "Jormungandr-Onboarding::send_to_sinacor_registration_queue::Error when trying send message to Iara"


class ErrorToUpdateUser(Exception):
    msg = (
        "Jormungandr-Onboarding::update_user_with_complementary_data::Error on trying to update user in mongo_db::"
        "User not exists, or unique_id invalid"
    )


class UserUniqueIdNotExists(Exception):
    msg = "Jormungandr-Onboarding::get_registration_data::Not exists an user_data with this unique_id"


class InvalidEmail(Exception):
    msg = "Invalid email address"


class OnboardingStepsStatusCodeNotOk(Exception):
    msg = "Jormungandr-Onboarding::get_user_current_step::Error when trying to get onboarding steps br"


class InvalidOnboardingCurrentStep(Exception):
    msg = "Jormungandr-Onboarding::validate_current_onboarding_step::User is not in the data validation step: {}"


class InvalidOnboardingAntiFraud(Exception):
    msg = "Jormungandr-Onboarding::validate_current_onboarding_step::User anti_fraud validation not approved"


class ErrorOnGetUniqueId(Exception):
    msg = "Jormungandr-Onboarding::get_unique_id::Fail when trying to get unique_id"


class FailedToGetData(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: internal server error"


class InvalidActivity(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid activity"


class HighRiskActivityNotAllowed(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: high risk activity not allowed"


class CriticalRiskClientNotAllowed(Exception):
    msg = "Jormungandr-Onboarding::validators::Critical risk client not allowed"


class InvalidState(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid state"


class InvalidCity(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid city"


class InvalidNationality(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid nationality"


class InvalidMaritalStatus(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid marital status"


class InvalidCountryAcronym(Exception):
    msg = "Jormungandr-Onboarding::validators::Invalid param: invalid country acronym"


class DeviceInfoRequestFailed(Exception):
    msg = "Error trying to get device info"


class DeviceInfoNotSupplied(Exception):
    msg = "Device info not supplied"
