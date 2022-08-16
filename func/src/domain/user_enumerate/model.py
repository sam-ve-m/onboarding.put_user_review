# Standards
from typing import List, Dict


class UserEnumerateDataModel:
    def __init__(self, payload_validated):
        self.user_review_data = payload_validated

    async def get_activity(self) -> int:
        activity_code = (
            self.user_review_data.get("personal", {})
            .get("occupation_activity", {})
            .get("value", False)
        )
        if not activity_code:
            raise ValueError("Occupation activity is required")
        return activity_code

    async def get_combination_birth_place(self) -> Dict:
        personal_country = (
            self.user_review_data.get("personal", {})
            .get("birth_place_country", {})
            .get("country", False)
        )
        personal_state = (
            self.user_review_data.get("personal", {})
            .get("birth_place_state", {})
            .get("value", False)
        )
        personal_city = (
            self.user_review_data.get("personal", {})
            .get("birth_place_city", {})
            .get("value", False)
        )
        birth_place_combination = {
            "country": personal_country,
            "state": personal_state,
            "city": personal_city,
        }
        if not all([personal_city, personal_state, personal_country]):
            raise ValueError("Birth place value is required")
        return birth_place_combination

    async def get_combination_address(self) -> Dict:
        country_address = (
            self.user_review_data.get("address", {})
            .get("country", {})
            .get("country", False)
        )
        state_address = (
            self.user_review_data.get("address", {})
            .get("state", {})
            .get("value", False)
        )
        city_address = (
            self.user_review_data.get("address", {}).get("city", {}).get("value", False)
        )
        address_combination = {
            "country": country_address,
            "state": state_address,
            "city": city_address,
        }
        if not all([city_address, state_address, country_address]):
            raise ValueError("Address values is required")
        return address_combination

    async def get_country_foreign_account_tax(self) -> List:
        foreign_account_tax = (
            self.user_review_data.get("personal", {})
            .get("tax_residences", {})
        )
        if not foreign_account_tax:
            return []
        foreign_account_tax_list = foreign_account_tax.get("value", {})
        if not foreign_account_tax_list:
            raise ValueError("Foreign account tax value is required")
        countries = list()
        for tax_residence in foreign_account_tax_list:
            countries.append(tax_residence.get("country", {}))
        if not all(countries):
            raise ValueError("Country from foreign account tax value is required")
        return countries

    async def get_document_state(self) -> str:
        document_state = (
            self.user_review_data.get("documents", {})
            .get("state", {})
            .get("value", False)
        )
        if not document_state:
            raise ValueError("State value is required")
        return document_state

    async def get_marital_status(self):
        marital_code = (
            self.user_review_data.get("marital", {})
            .get("status", {})
            .get("value", False)
        )
        if not marital_code:
            raise ValueError("Marital status is required")
        return marital_code

    async def get_nationalities(self) -> List:
        personal_nationality = (
            self.user_review_data.get("personal", {})
            .get("nationality", {})
            .get("value", False)
        )
        current_marital_status = (
            self.user_review_data.get("marital", {})
            .get("spouse", False)
        )
        nationalities = [personal_nationality]
        if current_marital_status:
            spouse_nationality = (
                self.user_review_data.get("marital", {}).get("spouse", {}).get("nationality", self._raise())

            )
            nationalities.append(spouse_nationality)
            if not all(nationalities):
                raise ValueError("Nationality value is required")
            return nationalities
        return nationalities

    @staticmethod
    async def _raise():
        raise ValueError("Value is required")
