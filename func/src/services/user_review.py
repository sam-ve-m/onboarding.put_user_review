# Jormungandr
from ..domain.exceptions import UserUniqueIdNotExists, ErrorOnUpdateUser
from ..domain.user_review.model import UserReviewModel
from ..repositories.mongo_db.user.repository import UserRepository
from ..services.builders.user_registration_update import UpdateCustomerRegistrationBuilder
from ..transports.audit.transport import Audit


class UserReviewDataService:
    def __init__(self, user_review_data_validated, unique_id):
        self.unique_id = unique_id
        self.user_review_data = user_review_data_validated

    async def apply_rules_to_update_user_review(self):
        user_data = await self._get_user_data(unique_id=self.unique_id)
        new_user_registration_data, modified_register_data = UpdateCustomerRegistrationBuilder(
            old_personal_data=user_data,
            new_personal_data=self.user_review_data,
            unique_id=self.unique_id
        ).build()
        user_review_model = UserReviewModel(
            user_review_data=self.user_review_data,
            unique_id=self.unique_id,
            modified_register_data=modified_register_data,
            new_user_registration_data=new_user_registration_data
        )
        await Audit.register_log(user_review_model=user_review_model)
        await self._update_user_review(
            unique_id=self.unique_id,
            new_user_registration_data=await user_review_model.get_new_user_data()
        )
        # TODO: implementar chamada ao client da Yara
        return True

    @staticmethod
    async def _get_user_data(unique_id: str) -> dict:
        user_data = await UserRepository.find_one_by_unique_id(unique_id=unique_id)
        if not user_data:
            raise UserUniqueIdNotExists
        return user_data

    @staticmethod
    async def _update_user_review(unique_id: str, new_user_registration_data: dict):
        user_updated = await UserRepository.update_one_with_user_review_data(
            unique_id=unique_id,
            new_user_registration_data=new_user_registration_data
        )
        if not user_updated.acknowledged:
            raise ErrorOnUpdateUser
        return True
