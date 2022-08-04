from ..repositories.oracle.repository import EnumerateRepository
from ..domain.exceptions import InvalidNationality, InvalidMaritalStatus, InvalidCountryAcronym, InvalidState, InvalidCity, InvalidActivity
from ..domain.user_enumerate.model import UserEnumerateDataModel
from typing import List


class EnumerateService:
    def __init__(self, user_review_data_validated: dict):
        self.user_review_data = user_review_data_validated
        self.user_enumerate_model = UserEnumerateDataModel(user_review_data_validated=user_review_data_validated)

    async def validate_enumerate_params(self) -> bool:
        activity_code = await self.user_enumerate_model.get_activity()
        await self._validate_activity(activity_code=activity_code)
        state = await self.user_enumerate_model.get_document_state()
        await self._validate_state(state=state)
        nationalities = await self.user_enumerate_model.get_nationalities()
        await self._validate_nationality(nationalities=nationalities)
        countries = await self.user_enumerate_model.get_country_foreign_account_tax()
        await self._validate_country_acronym(countries=countries)
        marital_code = await self.user_enumerate_model.get_marital_status()
        await self._validate_marital_status(marital_code=marital_code)
        address_combination = await self.user_enumerate_model.get_combination_address()
        await self._validate_combination_place(combination_place=address_combination)
        birth_place_combination = await self.user_enumerate_model.get_combination_birth_place()
        await self._validate_combination_place(combination_place=birth_place_combination)
        return True

    @staticmethod
    async def _validate_activity(activity_code: int) -> bool:
        result = await EnumerateRepository.get_activity(activity_code=activity_code)
        if not result:
            raise InvalidActivity
        return True

    @staticmethod
    async def _validate_country_acronym(countries) -> bool:
        if not countries:
            return True
        for country in countries:
            result = await EnumerateRepository.get_country(country_acronym=country)
            if not result:
                raise InvalidCountryAcronym
        return True

    @staticmethod
    async def _validate_marital_status(marital_code: int) -> bool:
        result = await EnumerateRepository.get_marital_status(marital_code=marital_code)
        if not result:
            raise InvalidMaritalStatus
        return True

    @staticmethod
    async def _validate_nationality(nationalities: List) -> bool:
        for nationality_code in nationalities:
            result = await EnumerateRepository.get_nationality(nationality_code=nationality_code)
            if not result:
                raise InvalidNationality
            return True

    @staticmethod
    async def _validate_state(state: str) -> bool:
        result = await EnumerateRepository.get_state(state=state)
        if not result:
            raise InvalidState
        return True

    @staticmethod
    async def _validate_combination_place(combination_place: dict) -> bool:
        result = await EnumerateRepository.get_city(
            country=combination_place.get("country"),
            state=combination_place.get("state"),
            id_city=combination_place.get("city"),
        )
        if not result:
            raise InvalidCity
        return True
