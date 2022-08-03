from ..domain.exceptions import UserUniqueIdNotExists
from ..repositories.mongo_db.user.repository import UserRepository


class UserReviewDataService:
    def __init__(self, user_data_validated, unique_id):
        self.unique_id = unique_id
        self.user_data_updated = user_data_validated.get("customer_registration_data")

    async def update_user_data_changes(self):
        user_data = self._get_user_data()
        pass

    async def _get_user_data(self) -> dict:
        user_data = await UserRepository.find_one_by_unique_id(unique_id=self.unique_id)
        if not user_data:
            raise UserUniqueIdNotExists
        return user_data
