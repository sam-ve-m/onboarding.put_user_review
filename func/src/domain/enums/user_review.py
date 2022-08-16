# Third party
from strenum import StrEnum


class PersonGender(StrEnum):
    MASCULINE = "M"
    FEMININE = "F"


class DocumentTypes(StrEnum):
    RG = "RG"
    CH = "CH"


class UserOnboardingStep(StrEnum):
    DATA_VALIDATION = "data_validation"
