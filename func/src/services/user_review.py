from etria_logger import Gladsheim
from regis import Regis, RegisResponse

from ..domain.enums.user_review import UserOnboardingStep
from ..domain.exceptions.exceptions import (
    UserUniqueIdNotExists,
    ErrorToUpdateUser,
    InvalidOnboardingCurrentStep,
    FailedToGetData,
    CriticalRiskClientNotAllowed,
)
from ..domain.user_review.model import UserReviewModel
from ..domain.user_review.validator import UserReviewData
from ..repositories.mongo_db.user.repository import UserRepository
from ..services.builders.user_registration_update import (
    UpdateCustomerRegistrationBuilder,
)
from ..transports.audit.transport import Audit
from ..transports.iara.transport import IaraClient
from ..transports.onboarding_steps.transport import OnboardingSteps


class UserReviewDataService:
    @staticmethod
    async def validate_current_onboarding_step(jwt: str) -> bool:
        user_current_step = await OnboardingSteps.get_user_current_step(jwt=jwt)
        if not user_current_step == UserOnboardingStep.DATA_VALIDATION:
            raise InvalidOnboardingCurrentStep(user_current_step)
        return True

    @staticmethod
    async def rate_client_risk(user_review_model: UserReviewModel):
        user_data = user_review_model.new_user_registration_data
        try:
            regis_response: RegisResponse = await Regis.rate_client_risk(
                patrimony=user_data["assets"]["patrimony"],
                address_city=user_data["address"]["city"],
                profession=user_data["occupation"]["activity"],
                is_pep=bool(user_data.get("is_pep")),
                is_pep_related=bool(user_data.get("is_pep_related")),
            )
        except Exception as error:
            Gladsheim.error(error=error, message="Error trying to rate client risk.")
            raise FailedToGetData()

        if not regis_response.risk_approval:
            raise CriticalRiskClientNotAllowed(
                f"unique_id: {user_review_model.unique_id,}, "
                f"score: {regis_response.risk_score}"
            )

        user_review_model.add_risk_data(risk_data=regis_response)

        await Audit.record_message_log_to_rate_client_risk(
            user_review_model=user_review_model
        )
        user_review_model.update_new_data_with_risk_data()

    @classmethod
    async def apply_rules_to_update_user_review(
        cls, unique_id: str, payload_validated: UserReviewData
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

        await cls.rate_client_risk(user_review_model)
        await Audit.record_message_log_to_update_registration_data(user_review_model)

        new_user_template = await user_review_model.get_new_user_data()
        await UserReviewDataService._update_user_review(
            unique_id=unique_id,
            new_user_registration_data=new_user_template,
        )
        await IaraClient.send_to_sinacor_registration_queue(
            user_model=user_review_model
        )
        return True

    @staticmethod
    async def _get_user_data(unique_id: str) -> dict:
        user_data = await UserRepository.find_one_by_unique_id(unique_id=unique_id)
        if not user_data:
            raise UserUniqueIdNotExists()
        return user_data

    @staticmethod
    async def _update_user_review(
        unique_id: str, new_user_registration_data: dict
    ) -> bool:
        user_updated = await UserRepository.update_one_with_user_review_data(
            unique_id=unique_id, new_user_registration_data=new_user_registration_data
        )
        if not user_updated.matched_count:
            raise ErrorToUpdateUser()
        return True

    @staticmethod
    async def _update_user(unique_id: str, new_data: dict) -> bool:
        user_updated = await UserRepository.update_user(
            unique_id=unique_id, new_data=new_data
        )
        if not user_updated.matched_count:
            raise ErrorToUpdateUser()
        return True
