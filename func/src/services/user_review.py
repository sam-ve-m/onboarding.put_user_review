# Jormungandr
from ..domain.enums.user_review import UserOnboardingStep
from ..domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    ErrorOnUpdateUser,
    InvalidOnboardingCurrentStep,
)

from ..domain.user_review.model import UserReviewModel
from ..repositories.mongo_db.user.repository import UserRepository
from ..services.builders.user_registration_update import (
    UpdateCustomerRegistrationBuilder,
)
from ..transports.audit.transport import Audit
from ..transports.onboarding_steps.transport import OnboardingSteps
from ..transports.iara.transport import IaraClient


class UserReviewDataService:
    @staticmethod
    async def validate_current_onboarding_step(jwt: str) -> bool:
        user_current_step = await OnboardingSteps.get_user_current_step(jwt=jwt)
        if not user_current_step == UserOnboardingStep.DATA_VALIDATION:
            raise InvalidOnboardingCurrentStep
        return True

    @staticmethod
    async def apply_rules_to_update_user_review(
        unique_id: str, payload_validated: dict
    ) -> bool:
        user_data = await UserReviewDataService._get_user_data(unique_id=unique_id)
        (
            new_user_registration_data,
            modified_register_data,
        ) = UpdateCustomerRegistrationBuilder(
            old_personal_data=user_data,
            new_personal_data=payload_validated,
            unique_id=unique_id,
        ).build()
        user_review_model = UserReviewModel(
            user_review_data=payload_validated,
            unique_id=unique_id,
            modified_register_data=modified_register_data,
            new_user_registration_data=new_user_registration_data,
        )
        await Audit.register_log(user_review_model=user_review_model)
        await UserReviewDataService._update_user_review(
            unique_id=unique_id,
            new_user_registration_data=await user_review_model.get_new_user_data(),
        )
        await IaraClient.send_to_sinacor_registration_queue(
            user_model=user_review_model
        )
        return True

    @staticmethod
    async def _get_user_data(unique_id: str) -> dict:
        user_data = await UserRepository.find_one_by_unique_id(unique_id=unique_id)
        if not user_data:
            raise UserUniqueIdNotExists
        return user_data

    @staticmethod
    async def _update_user_review(
        unique_id: str, new_user_registration_data: dict
    ) -> bool:
        user_updated = await UserRepository.update_one_with_user_review_data(
            unique_id=unique_id, new_user_registration_data=new_user_registration_data
        )
        if not user_updated.acknowledged:
            raise ErrorOnUpdateUser
        return True
