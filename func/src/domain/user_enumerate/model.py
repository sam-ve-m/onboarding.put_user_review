# Jormungandr - Onboarding
from ...domain.user_review.validator import UserReviewData

# Standards
from typing import List, Dict


class UserEnumerateDataModel:
    def __init__(self, payload_validated: UserReviewData):
        self.user_review_data = payload_validated.dict()

    async def get_activity(self) -> int:
        activity_code = (
            self.user_review_data.get("personal", {})
            .get("occupation_activity", {})
            .get("value")
        )
        if not activity_code:
            raise ValueError("Occupation activity is required")
        return activity_code

    async def get_combination_birth_place(self) -> Dict:
        personal_country = (
            self.user_review_data.get("personal", {})
            .get("birth_place_country", {})
            .get("value")
        )
        personal_state = (
            self.user_review_data.get("personal", {})
            .get("birth_place_state", {})
            .get("value")
        )
        personal_city = (
            self.user_review_data.get("personal", {})
            .get("birth_place_city", {})
            .get("value")
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
            self.user_review_data.get("address", {}).get("country", {}).get("value")
        )
        state_address = (
            self.user_review_data.get("address", {}).get("state", {}).get("value")
        )
        city_address = (
            self.user_review_data.get("address", {}).get("city", {}).get("value")
        )
        address_combination = {
            "country": country_address,
            "state": state_address,
            "city": city_address,
        }
        if not all([city_address, state_address, country_address]):
            raise ValueError("Address values is required")
        return address_combination

    async def get_country_tax_residences(self) -> List:
        tax_residences = self.user_review_data.get("personal", {}).get("tax_residences")
        if not tax_residences:
            return []
        tax_residences_list = tax_residences.get("value")
        if not tax_residences_list:
            raise ValueError("Value key is required")
        countries = [
            tax_residence.get("country") for tax_residence in tax_residences_list
        ]
        if not all(countries):
            raise ValueError("Country from foreign account tax value is required")
        return countries

    async def get_document_state(self) -> str:
        document_state = (
            self.user_review_data.get("documents", {}).get("state", {}).get("value")
        )
        if not document_state:
            raise ValueError("State value is required")
        return document_state

    async def get_marital_status(self):
        marital_code = (
            self.user_review_data.get("marital", {}).get("status", {}).get("value")
        )
        if not marital_code:
            raise ValueError("Marital status is required")
        return marital_code

    async def get_nationalities(self) -> List:
        personal_nationality = (
            self.user_review_data.get("personal", {})
            .get("nationality", {})
            .get("value")
        )
        current_marital_status = self.user_review_data.get("marital", {}).get("spouse")
        nationalities = [personal_nationality]
        if current_marital_status:
            spouse_nationality = (
                self.user_review_data.get("marital", {})
                .get("spouse", {})
                .get("nationality")
            )
            nationalities.append(spouse_nationality)
            if not all(nationalities):
                raise ValueError("Nationality value is required")
            return nationalities
        return nationalities
