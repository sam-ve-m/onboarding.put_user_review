from ..domain.exceptions import UserUniqueIdNotExists
from ..domain.user_review.model import UserReviewModel
from ..repositories.mongo_db.user.repository import UserRepository
from ..services.builders.user_registration_update import UpdateCustomerRegistrationBuilder
from ..transports.audit.transport import Audit


class UserReviewDataService:
    def __init__(self, user_review_data_validated, unique_id):
        self.unique_id = unique_id
        self.user_review_data = user_review_data_validated

    async def update_user_data_changes(self):
        user_data = await self._get_user_data()
        new_customer_registration_data, modified_register_data = UpdateCustomerRegistrationBuilder(
            old_personal_data=user_data,
            new_personal_data=self.user_review_data,
            unique_id=self.unique_id
        ).build()
        user_review_model = UserReviewModel(
            user_review_data_validated=self.user_review_data,
            unique_id=self.unique_id,
            modified_register_data=modified_register_data
        )
        # Sindri.dict_to_primitive_types(user_update_register_schema)
        await Audit.register_log(user_review_model=user_review_model)
        pass

    async def _get_user_data(self) -> dict:
        user_data = await UserRepository.find_one_by_unique_id(unique_id=self.unique_id)
        if not user_data:
            raise UserUniqueIdNotExists
        return user_data
