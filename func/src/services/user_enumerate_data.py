from ..repositories.oracle.repository import EnumerateRepository
from ..domain.exceptions import InvalidNationality, InvalidMaritalStatus, InvalidCountryAcronym, InvalidState

from typing import List


class EnumerateService:
    def __init__(self, user_review_data_validated: dict):
        self.user_review_data = user_review_data_validated
        self.user_enumerate_model = EnumerateModel(user_review_data_validated)

    async def validate_enumerate_params(self) -> bool:
        await self._validate_nationality()
        await self._validate_country_acronym()
        await self._validate_marital_status()
        return True

    async def _validate_country_acronym(self) -> bool:
        foreign_account_tax = self.user_review_data.get("foreign_account_tax")
        if not self.user_enumerate_model.foreign_account_tax:
            return True
        for tax_residence in foreign_account_tax:
            country_acronym = tax_residence.get("country")
            result = await EnumerateRepository.get_country(country_acronym=country_acronym)
            if not result:
                raise InvalidCountryAcronym
        return True

    async def _validate_marital_status(self) -> bool:
        code = self.user_review_data.get("marital_status")
        result = await EnumerateRepository.get_marital_status(code=code)
        if not result:
            raise InvalidMaritalStatus
        return True

    async def _validate_nationality(self) -> bool:
        spouse = self.user_review_data.get("spouse")
        if not spouse:
            return True
        nationality_code = spouse.get("nationality")
        result = await EnumerateRepository.get_nationality(code=nationality_code)
        if not result:
            raise InvalidNationality
        return True

    @staticmethod
    async def _validate_state(states: List) -> bool:
        for state in states:
            result = await EnumerateRepository.get_state(state=state)
            if not result:
                raise InvalidState
        return True

    async def _get_states(self):
        states = list()
        address_state = self.user_review_data.get("address", {}).get("state", False)
        personal_state = self.user_review_data.get("personal", {}).get("birth_place_state", False)
        documents_state = self.user_review_data.get("documents", {}).get("state", False)
        if not all([address_state, documents_state, personal_state]):
            raise InvalidState
        states.append(address_state)
        states.append(personal_state)k
        states.append(documents_state)
        await self._validate_state(states=states)
