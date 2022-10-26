# Jormungandr - Onboarding
from ...domain.exceptions.exceptions import OnboardingStepsStatusCodeNotOk

# Standards
from http import HTTPStatus

# Third party
from decouple import config
from httpx import AsyncClient

from ...domain.models.onboarding import Onboarding


class OnboardingSteps:
    @staticmethod
    async def get_user_current_step(jwt: str) -> Onboarding:
        headers = {"x-thebes-answer": jwt}
        async with AsyncClient() as httpx_client:
            request_result = await httpx_client.get(
                config("ONBOARDING_STEPS_BR_URL"), headers=headers
            )
            if not request_result.status_code == HTTPStatus.OK:
                raise OnboardingStepsStatusCodeNotOk()
            user_current_step = (
                request_result.json().get("result", {}).get("current_step")
            )
            anti_fraud_status = (
                request_result.json().get("result", {}).get("anti_fraud")
            )
        onboarding_step = Onboarding(
            step=user_current_step, anti_fraud=anti_fraud_status
        )
        return onboarding_step
