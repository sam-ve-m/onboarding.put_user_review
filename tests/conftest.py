# Jormungandr - Onboarding
from func.src.domain.user_enumerate.model import UserEnumerateDataModel
from func.src.services.user_enumerate_data import UserEnumerateService
from tests.src.services.user_review.stubs import stub_payload_validated, stub_payload_missing_data, StubUserReview

# Third party
from pytest import fixture
from unittest.mock import patch


@fixture(scope="function")
def enumerate_service_empty():
    service = UserEnumerateService(payload_validated=stub_payload_validated)
    return service


@fixture(scope="function")
def enumerate_model():
    enumerate_model = UserEnumerateDataModel(
        payload_validated=stub_payload_validated
    )
    return enumerate_model


@fixture(scope="function")
def enumerate_model_missing_data():
    enumerate_model = UserEnumerateDataModel(
        payload_validated=StubUserReview
    )
    return enumerate_model
