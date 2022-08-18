# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
async def test_when_valid_activity_then_returns_activity_code(enumerate_model):
    activity_code = await enumerate_model.get_activity()

    assert isinstance(activity_code, int)
    assert activity_code == 155


@pytest.mark.asyncio
async def test_when_invalid_activity_then_raises(enumerate_model_missing_data):
    with pytest.raises(ValueError):
        await enumerate_model_missing_data.get_activity()


@pytest.mark.asyncio
async def test_when_valid_birth_place_then_return_combination_birth_place(
    enumerate_model,
):
    birth_place_combination = await enumerate_model.get_combination_birth_place()

    assert isinstance(birth_place_combination, dict)
    assert birth_place_combination.get("country") == "BRA"
    assert birth_place_combination.get("state") == "SP"
    assert birth_place_combination.get("city") == 5150


@pytest.mark.asyncio
async def test_when_invalid_birth_place_combination_then_raises(enumerate_model_missing_data):
    with pytest.raises(ValueError):
        await enumerate_model_missing_data.get_combination_birth_place()


@pytest.mark.asyncio
async def test_when_valid_address_then_return_address_combination(enumerate_model):
    address_combination = await enumerate_model.get_combination_address()

    assert isinstance(address_combination, dict)
    assert address_combination.get("country") == "BRA"
    assert address_combination.get("state") == "SP"
    assert address_combination.get("city") == 5150


@pytest.mark.asyncio
async def test_when_invalid_address_combination_then_raises(enumerate_model_missing_data):
    with pytest.raises(ValueError):
        await enumerate_model_missing_data.get_combination_address()


@pytest.mark.asyncio
async def test_when_have_foreign_account_tax_then_return_countries(enumerate_model):
    countries = await enumerate_model.get_country_foreign_account_tax()

    assert isinstance(countries, list)
    assert countries[0] == "EUA"
    assert countries[1] == "ING"


@pytest.mark.asyncio
async def test_when_no_foreign_account_tax_then_return_empty_list(
        enumerate_model_missing_data,
):
    countries = await enumerate_model_missing_data.get_country_foreign_account_tax()

    assert isinstance(countries, list)
    assert countries == []


@pytest.mark.asyncio
@patch('func.src.domain.user_enumerate.model.UserEnumerateDataModel.map_foreign_account_tax_possibilities', side_effect=[True, ValueError])
async def test_when_invalid_foreign_tax_then_raises(enumerate_model):
    with pytest.raises(ValueError):
        await enumerate_model.get_country_foreign_account_tax()


@pytest.mark.asyncio
async def test_when_valid_document_state_then_return_document_state(enumerate_model):
    document_state = await enumerate_model.get_document_state()

    assert isinstance(document_state, str)
    assert document_state == "SP"


@pytest.mark.asyncio
async def test_when_valid_marital_status_then_return_marital_code(enumerate_model):
    marital_code = await enumerate_model.get_marital_status()

    assert isinstance(marital_code, int)
    assert marital_code == 1


@pytest.mark.asyncio
async def test_when_valid_nationalities_then_return_all_nationalities(enumerate_model):
    nationalities = await enumerate_model.get_nationalities()

    assert isinstance(nationalities, list)
    assert nationalities[0] == 1
