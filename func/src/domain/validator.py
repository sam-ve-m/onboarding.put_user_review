from pydantic import BaseModel, constr, validator
from typing import Optional, List
from datetime import datetime, timezone

# from .exceptions import InvalidEmail
from func.src.domain.exceptions import InvalidEmail
from func.src.domain.enums.user_review import PersonGender, DocumentTypes
import re


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


from copy import deepcopy


class CnpjSource(Source):
    value: str

    @validator('value', always=True, allow_reuse=True)
    def format_cnpj(cls, cnpj):
        return list(re.sub(r'[^0-9]', '', cnpj))

    @validator('value', always=True, allow_reuse=True)
    def cnpj_is_not_a_sequence(cls, cnpj):
        if cnpj == cnpj[::-1]:
            raise ValueError("Invalid CNPJ")
        return cnpj

    @validator('value', always=True, allow_reuse=True)
    def cnpj_calculation(cls, new_cnpj):
        cnpj_origin = deepcopy(new_cnpj)
        del new_cnpj[-2:]
        first_digit_calculation_array = ['5', '4', '3', '2', '9', '8', '7', '6', '5', '4', '3', '2']
        calc_cnpj = 11 - ((sum([int(x) * int(y)
                                for x, y in zip(first_digit_calculation_array, new_cnpj)
                                ])) % 11)
        calc_cnpj = calc_cnpj if calc_cnpj < 10 else 0
        new_cnpj.append(str(calc_cnpj))
        second_digit_calculation_array = ['6', '5', '4', '3', '2', '9', '8', '7', '6', '5', '4', '3', '2']
        calc_cnpj = 11 - ((sum([int(x) * int(y)
                                for x, y in zip(second_digit_calculation_array, new_cnpj)
                                ])) % 11)
        calc_cnpj = calc_cnpj if calc_cnpj < 10 else 0
        new_cnpj.append(str(calc_cnpj))
        if not cnpj_origin == new_cnpj:
            raise ValueError("Invalid CNPJ")
        return new_cnpj


class CpfSource(Source):
    cpf: str

    @validator("cpf", always=True, allow_reuse=True)
    def format_cpf(cls, cpf: str):
        cpf = re.sub("[^0-9]", "", cpf)
        return cpf

    @validator('cpf', always=True, allow_reuse=True)
    def cpf_is_not_a_sequence(cls, cpf):
        if cpf == cpf[::-1]:
            raise ValueError("Invalid CPF")
        return cpf

    @validator("cpf", always=True, allow_reuse=True)
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

    @validator("value", always=True, allow_reuse=True)
    def validate_email(cls, email: str):
        regex = r'^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{2,66})\.([a-z]{2,3}(?:\.[a-z]{2})?)$'
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
    value: constr(regex=r"^[a-zA-Z\sáéíóúãẽĩõũâêîôûç]+$")


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
    occupation_activity: Optional[ActivitySource]  # TODO: verificar o tipo de dado que deve vir, para consultar na oracle
    company_name: Optional[CompanyNameSource]
    company_cnpj: Optional[CnpjSource]
    patrimony: Optional[PatrimonySource]
    income: Optional[IncomeSource]
    tax_residences: Optional[TaxResidenceSource] = []
    birth_place_country: Optional[CountrySource]
    birth_place_state: Optional[StateSource]  # TODO: verificar o tipo de dado que deve vir, para consultar na oracle
    birth_place_city: Optional[CountySource]  # TODO: verificar o tipo de dado que deve vir, para consultar na oracle


class UserMaritalDataSource(BaseModel):
    status: MaritalStatusSource
    spouse: Optional[SpouseSource]


class UserDocumentsDataUpdate(BaseModel):
    cpf: Optional[CpfSource]
    identity_type: Optional[DocumentTypesSource]
    identity_number: Optional[DocumentNumberSource]
    expedition_date: Optional[DateSource]
    issuer: Optional[IssuerSource]
    state: Optional[StateSource]  # TODO: verificar o tipo de dado que deve vir, para consultar na oracle


class UserAddressDataUpdate(BaseModel):
    country: Optional[CountrySource]
    state: Optional[StateSource]  # TODO: verificar o tipo de dado que deve vir, para consultar na oracle
    city: Optional[CountySource]  # TODO: verificar o tipo de dado que deve vir, para consultar na oracle
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
