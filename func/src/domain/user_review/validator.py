# Jormungandr - Onboarding
from validate_docbr import CNPJ, CPF

from ..enums.high_risk_activity import HighRiskActivity
from ...domain.enums.user_review import PersonGender, DocumentTypes
from ..exceptions.exceptions import (
    InvalidEmail,
    HighRiskActivityNotAllowed,
    FinancialCapacityNotValid,
)

# Standards
from copy import deepcopy
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import re

# Third party
from pydantic import BaseModel, constr, validator, root_validator


class Source(BaseModel):
    source: str


class ActivitySource(Source):
    value: int

    @validator("value")
    def occupation_cannot_be_high_risk(cls, occupation):
        try:
            HighRiskActivity(occupation)
        except ValueError:
            return occupation
        raise HighRiskActivityNotAllowed()


class AddressNumberSource(Source):
    value: str


class UsPersonSource(Source):
    value: bool


class BirthDateSource(Source):
    value: int

    @validator("value")
    def validate_value(cls, value):
        try:
            date = datetime.fromtimestamp(value, tz=timezone.utc)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class CelPhoneSource(Source):
    value: constr(regex=r"^\+\d+", min_length=14, max_length=14)


class CompanyNameSource(Source):
    value: str


class CnpjSource(Source):
    value: str

    @validator("value")
    def validate_cnpj(cls, cnpj: str):
        return_cnpj = CNPJ().validate(cnpj)
        if return_cnpj is False:
            raise ValueError("Invalid CNPJ")
        return cnpj


class CpfSource(Source):
    value: str

    @validator("value")
    def validate_cpf(cls, cpf: str):
        return_cpf = CPF().validate(cpf)
        if return_cpf is False:
            raise ValueError(f"Invalid cpf")
        return cpf


class CountrySource(Source):
    value: constr(min_length=3, max_length=3)


class CountySource(Source):
    value: int


class DateSource(Source):
    value: int

    @validator("value")
    def validate_value(cls, value):
        try:
            date = datetime.fromtimestamp(value)
            return date
        except Exception:
            raise ValueError("Wrong timestamp supplied")


class DocumentNumberSource(Source):
    value: str

    @validator("value")
    def validate_value(cls, value):
        return value.replace(".", "").replace("-", "").replace("/", "")


class DocumentTypesSource(Source):
    value: DocumentTypes


class EmailSource(Source):
    value: str

    @validator("value")
    def validate_email(cls, email: str):
        regex = r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{1,66})\.([a-z]{2,3}(?:\.[a-z]{2})?)$"
        if not re.search(regex, email):
            raise InvalidEmail
        return email


class GenderSource(Source):
    value: PersonGender


class IncomeSource(Source):
    value: float


class IssuerSource(Source):
    value: str


char_with_space = "[a-zA-Z\sáéíóúãẽĩõũâêîôûÁÉÍÓÚÃẼĨÕŨÂÊÎÔÛç]"
char_without_space = "[a-zA-ZáéíóúãẽĩõũâêîôûÁÉÍÓÚÃẼĨÕŨÂÊÎÔÛç]"
name_regex = rf"^{char_without_space}+\s{char_without_space}{char_with_space}*$"


class NameSource(Source):
    value: constr(regex=name_regex, max_length=60)


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
    cpf: Optional[CpfSource]
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
    tax_residences: Optional[TaxResidenceSource]
    us_person: UsPersonSource
    birth_place_country: CountrySource
    birth_place_state: StateSource
    birth_place_city: CountySource

    @root_validator(pre=True)
    def validate_financial_capacity(cls, values: Dict[str, Any]):
        patrimony = values.get("patrimony", {}).get("value")
        income = values.get("income", {}).get("value")
        if (patrimony + income) < 1000:
            raise FinancialCapacityNotValid()
        return values


class UserMaritalDataSource(BaseModel):
    status: MaritalStatusSource
    spouse: Optional[SpouseSource]


class UserDocumentsDataValidation(BaseModel):
    cpf: CpfSource
    identity_type: DocumentTypesSource
    identity_number: DocumentNumberSource
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
