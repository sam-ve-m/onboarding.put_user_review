from pydantic import BaseModel, constr, validator
from typing import Optional, List
from datetime import datetime, timezone

from .exceptions import InvalidEmail
from func.src.domain.enums.user_review import PersonGender, DocumentTypes
from etria_logger import Gladsheim
import re


class Source(BaseModel):
    source: str


class AddressNumberSource(Source):
    value: str


class BirthDateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, value):
        try:
            date = datetime.fromtimestamp(value, tz=timezone.utc)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class CelPhoneSource(Source):
    value: constr(regex=r"^\+\d+", min_length=13, max_length=14)


class CompanyNameSource(Source):
    value: str


class CpfSource(Source):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str):
        cpf = re.sub("[^0-9]", "", cpf)
        return cpf

    @validator("cpf", always=True, allow_reuse=True)
    def validate_cpf(cls, cpf: str):
        cpf_last_digits = cpf[:-2]
        cont_reversed = 10
        total = 0

        for index in range(19):
            if index > 8:
                index -= 9
            total += int(cpf_last_digits[index]) * cont_reversed
            cont_reversed -= 1

            if cont_reversed < 2:
                cont_reversed = 11
                digits = 11 - (total % 11)

                if digits > 9:
                    digits = 0
                total = 0
                cpf_last_digits += str(digits)

        sequence = cpf_last_digits == str(cpf_last_digits[0]) * len(cpf)
        if not cpf == cpf_last_digits or sequence:
            raise ValueError("invalid cpf")
        return cpf


class CountrySource(Source):
    country: constr(min_length=3, max_length=3)


class CountySource(Source):
    value: int


class DateSource(Source):
    value: int

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, value):
        try:
            date = datetime.fromtimestamp(value)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class DocumentNumberSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def validate_value(cls, value):
        return value.replace(".", "").replace("-", "").replace("/", "")


class DocumentTypesSource(Source):
    value: DocumentTypes


class EmailSource(Source):
    value: str

    @validator("email")
    def validate_email(cls, email: str):
        regex = r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{2,66})\.([a-z]{2,3}(?:\.[a-z]{2})?)$'
        if not re.search(regex, email):
            Gladsheim.error(message=f"Validator::validate_email::Invalid email format::{email}")
            raise InvalidEmail
        return email


class GenderSource(Source):
    value: PersonGender


class IncomeSource(Source):
    value: float


class IssuerSource(Source):
    value: str


class NameSource(Source):
    value: constr(regex=r"^[a-zA-Z\sáéíóúãẽĩõũâêîôûç]+$")


class NationalitySource(Source):
    value: int


class NeighborhoodSource(Source):
    value: constr(min_length=3, max_length=18)


class NickNameSource(Source):
    value: str


class PatrimonySource(Source):
    value: float


class PhoneSource(Source):
    value: constr(regex=r"^\+\d+", min_length=13, max_length=14)


class SpouseSource(BaseModel):
    name: NameSource
    cpf: CpfSource
    nationality: NationalitySource


class StreetNameSource(Source):
    value: constr(min_length=3, max_length=30)


class TaxResidence(BaseModel):
    country: constr(min_length=3, max_length=3)
    tax_number: str


class TaxResidenceSource(Source):
    value: List[TaxResidence]



class ZipCodeSource(Source):
    value: constr(regex=r"^[0-9]{5}-[\d]{3}")


class UserPersonalDataUpdate(BaseModel):
    name: Optional[NameSource]
    nick_name: Optional[NickNameSource]
    birth_date: Optional[BirthDateSource]
    gender: Optional[GenderSource]
    father_name: Optional[NameSource]
    mother_name: Optional[NameSource]
    email: Optional[EmailSource]
    phone: Optional[CelPhoneSource]
    nationality: Optional[NationalitySource]
    occupation_activity: Optional[ActivitySource]
    company_name: Optional[CompanyNameSource]
    company_cnpj: Optional[CnpjSource]
    patrimony: Optional[PatrimonySource]
    income: Optional[IncomeSource]
    tax_residences: Optional[TaxResidenceSource] = []
    birth_place_country: Optional[CountrySource]
    birth_place_state: Optional[StateSource]
    birth_place_city: Optional[CountySource]


class UserMaritalDataSource(BaseModel):
    status: MaritalStatusSource
    spouse: Optional[SpouseSource]


class UserDocumentsDataUpdate(BaseModel):
    cpf: Optional[CpfSource]
    identity_type: Optional[DocumentTypesSource]
    identity_number: Optional[DocumentNumberSource]
    expedition_date: Optional[DateSource]
    issuer: Optional[IssuerSource]
    state: Optional[StateSource]


class UserAddressDataUpdate(BaseModel):
    country: Optional[CountrySource]
    state: Optional[StateSource]
    city: Optional[CountySource]
    neighborhood: Optional[NeighborhoodSource]
    street_name: Optional[StreetNameSource]
    number: Optional[AddressNumberSource]
    zip_code: Optional[ZipCodeSource]
    phone: Optional[PhoneSource]


class UserUpdateData(BaseModel):
    personal: Optional[UserPersonalDataUpdate]
    marital: Optional[UserMaritalDataSource]
    documents: Optional[UserDocumentsDataUpdate]
    address: Optional[UserAddressDataUpdate]
