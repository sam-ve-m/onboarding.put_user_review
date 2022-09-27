# Jormungandr - Onboarding
from ...domain.enums.user_review import PersonGender, DocumentTypes
from ..exceptions.exceptions import InvalidEmail

# Standards
from copy import deepcopy
from typing import Optional, List
from datetime import datetime, timezone
import re

# Third party
from pydantic import BaseModel, constr, validator


class Source(BaseModel):
    source: str


class ActivitySource(Source):
    value: int


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


class CnpjSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def format_cnpj(cls, cnpj):
        return list(re.sub(r"[^0-9]", "", cnpj))

    @validator("value", always=True, allow_reuse=True)
    def cnpj_is_not_a_sequence(cls, cnpj):
        if cnpj == cnpj[::-1]:
            raise ValueError("Invalid CNPJ")
        return cnpj

    @validator("value", always=True, allow_reuse=True)
    def cnpj_calculation(cls, new_cnpj):
        first_digit_calculation_array = [
            "5",
            "4",
            "3",
            "2",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
        ]
        second_digit_calculation_array = [
            "6",
            "5",
            "4",
            "3",
            "2",
            "9",
            "8",
            "7",
            "6",
            "5",
            "4",
            "3",
            "2",
        ]
        cnpj_origin = deepcopy(new_cnpj)
        del new_cnpj[-2:]

        calc_cnpj = 11 - (
            (
                sum(
                    [
                        int(x) * int(y)
                        for x, y in zip(first_digit_calculation_array, new_cnpj)
                    ]
                )
            )
            % 11
        )
        calc_cnpj = calc_cnpj if calc_cnpj < 10 else 0
        new_cnpj.append(str(calc_cnpj))

        calc_cnpj = 11 - (
            (
                sum(
                    [
                        int(x) * int(y)
                        for x, y in zip(second_digit_calculation_array, new_cnpj)
                    ]
                )
            )
            % 11
        )
        calc_cnpj = calc_cnpj if calc_cnpj < 10 else 0
        new_cnpj.append(str(calc_cnpj))

        if not cnpj_origin == new_cnpj:
            raise ValueError("Invalid CNPJ")

        return new_cnpj


class CpfSource(Source):
    value: str

    @validator("value", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str):
        cpf = re.sub("[^0-9]", "", cpf)
        return cpf

    @validator("value", always=True, allow_reuse=True)
    def cpf_is_not_a_sequence(cls, cpf):
        if cpf == cpf[::-1]:
            raise ValueError("Invalid CPF")
        return cpf

    @validator("value", always=True, allow_reuse=True)
    def cpf_calculation(cls, cpf: str):
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
        if not cpf == cpf_last_digits:
            raise ValueError("Invalid CPF")
        return cpf


class CountrySource(Source):
    value: constr(min_length=3, max_length=3)


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

    @validator("value", always=True, allow_reuse=True)
    def validate_email(cls, email: str):
        regex = r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{2,66})\.([a-z]{2,3}(?:\.[a-z]{2})?)$"
        if not re.search(regex, email):
            raise InvalidEmail
        return email


class GenderSource(Source):
    value: PersonGender


class IncomeSource(Source):
    value: float


class IssuerSource(Source):
    value: str


class NameSource(Source):
    value: constr(regex=r"^[a-zA-Z\sáéíóúãẽĩõũâêîôûç]+$", max_length=60)


class NationalitySource(Source):
    value: int


class NeighborhoodSource(Source):
    value: constr(min_length=3, max_length=18)


class NickNameSource(Source):
    value: str


class MaritalStatusSource(Source):
    value: int


class PatrimonySource(Source):
    value: float


class PhoneSource(Source):
    value: constr(regex=r"^\+\d+", min_length=13, max_length=14)


class SpouseSource(BaseModel):
    name: NameSource
    cpf: CpfSource
    nationality: NationalitySource


class StateSource(Source):
    value: constr(min_length=2, max_length=2)


class StreetNameSource(Source):
    value: constr(min_length=3, max_length=30)


class TaxResidence(BaseModel):
    country: constr(min_length=3, max_length=3)
    tax_number: str


class TaxResidenceSource(Source):
    value: List[TaxResidence]


class ZipCodeSource(Source):
    value: constr(regex=r"^[0-9]{5}-[\d]{3}")


class ComplementSource(Source):
    value: constr(max_length=20)


class UserPersonalDataValidation(BaseModel):
    name: NameSource
    nick_name: NickNameSource
    birth_date: BirthDateSource
    gender: GenderSource
    father_name: Optional[NameSource]
    mother_name: NameSource
    email: EmailSource
    phone: CelPhoneSource
    nationality: NationalitySource
    occupation_activity: ActivitySource
    company_name: Optional[CompanyNameSource]
    company_cnpj: Optional[CnpjSource]
    patrimony: PatrimonySource
    income: IncomeSource
    foreign_account_tax: Optional[TaxResidenceSource]
    birth_place_country: CountrySource
    birth_place_state: StateSource
    birth_place_city: CountySource


class UserMaritalDataSource(BaseModel):
    status: MaritalStatusSource
    spouse: Optional[SpouseSource]


class UserDocumentsDataValidation(BaseModel):
    cpf: CpfSource
    identity_type: DocumentTypesSource
    identity_number: DocumentNumberSource
    expedition_date: DateSource
    issuer: IssuerSource
    state: StateSource


class UserAddressDataValidation(BaseModel):
    country: CountrySource
    state: StateSource
    city: CountySource
    neighborhood: NeighborhoodSource
    street_name: StreetNameSource
    number: AddressNumberSource
    zip_code: ZipCodeSource
    phone: Optional[PhoneSource]
    complement: Optional[ComplementSource]


class UserReviewData(BaseModel):
    personal: UserPersonalDataValidation
    marital: UserMaritalDataSource
    documents: UserDocumentsDataValidation
    address: UserAddressDataValidation
