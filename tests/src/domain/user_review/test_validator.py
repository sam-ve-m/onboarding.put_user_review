import pytest

from func.src.domain.exceptions.exceptions import (
    HighRiskActivityNotAllowed,
    InvalidEmail,
    FinancialCapacityNotValid,
)
from func.src.domain.user_review.validator import (
    UserReviewData,
    CpfSource,
    CnpjSource,
    EmailSource,
    UserPersonalDataValidation,
)

register_dummy = {
    "personal": {
        "name": {"source": "app", "value": "Rosa Jessica"},
        "nick_name": {"source": "app", "value": "Rosinha"},
        "birth_date": {"source": "app", "value": 158986800},
        "gender": {"source": "app", "value": "F"},
        "father_name": {"source": "app", "value": "Foi Eu"},
        "company_cnpj": {"source": "app", "value": "02916265000160"},
        "mother_name": {"source": "app", "value": "Rosa Mae"},
        "email": {"source": "app", "value": "brabo04@abraaoz.tk"},
        "phone": {"source": "app", "value": "+5577998636716"},
        "nationality": {"source": "app", "value": 1},
        "occupation_activity": {"source": "app", "value": 101},
        "patrimony": {"source": "app", "value": 12000},
        "income": {"source": "app", "value": 10000},
        "birth_place_country": {"source": "app", "value": "BRA"},
        "birth_place_state": {"source": "app", "value": "PA"},
        "birth_place_city": {"source": "app", "value": 2412},
        "us_person": {"source": "app", "value": True},
    },
    "marital": {"status": {"source": "app", "value": 1}},
    "documents": {
        "cpf": {"source": "app", "value": "72772117073"},
        "identity_type": {"source": "app", "value": "CH"},
        "identity_number": {"source": "app", "value": "06713096255"},
        "issuer": {"source": "app", "value": "SSP"},
        "state": {"source": "app", "value": "SP"},
    },
    "address": {
        "country": {"source": "app", "value": "BRA"},
        "state": {"source": "app", "value": "SP"},
        "city": {"source": "app", "value": 5051},
        "neighborhood": {"source": "app", "value": "Centro"},
        "street_name": {"source": "app", "value": "Praça Padre Domingos Segurado "},
        "number": {"source": "app", "value": "142"},
        "zip_code": {"source": "app", "value": "12980-970"},
        "complement": {"source": "app", "value": "complemento"},
    },
}


@pytest.mark.asyncio
async def test_validator_when_is_all_ok():
    data_validated = UserReviewData(**register_dummy)


@pytest.mark.asyncio
async def test_invalid_email():
    with pytest.raises(InvalidEmail):
        EmailSource.validate_email("svm.gmail.com")


@pytest.mark.asyncio
async def test_valid_email():
    response = EmailSource.validate_email("svm@gmail.com")
    assert response == "svm@gmail.com"


def test_validate_cpf_true():
    response = CpfSource.validate_cpf("72932652044")
    assert response == "72932652044"


def test_validate_cpf_false():
    with pytest.raises(ValueError) as error:
        response = CpfSource.validate_cpf("12345678910")


def test_validate_cnpj_true():
    response = CnpjSource.validate_cnpj("96564694000169")
    assert response == "96564694000169"


def test_validate_cnpj_false():
    with pytest.raises(ValueError) as error:
        response = CnpjSource.validate_cnpj("12123123123412")


stub_values_false = {"patrimony": {"value": 500}, "income": {"value": 500}}


def test_financial_capacity_false():
    response = UserPersonalDataValidation.validate_financial_capacity(values=stub_values_false)
    assert response == stub_values_false


stub_values_true = {"patrimony": {"value": 800}, "income": {"value": 100}}


def test_financial_capacity_true():
    with pytest.raises(FinancialCapacityNotValid):
        response = UserPersonalDataValidation.validate_financial_capacity(values=stub_values_true)
