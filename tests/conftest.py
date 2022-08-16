# Jormungandr - Onboarding
from func.src.domain.user_enumerate.model import UserEnumerateDataModel
from func.src.services.user_enumerate_data import UserEnumerateService
from tests.src.domain.enumerate.stubs import stub_payload

# Third party
from pytest import fixture


@fixture(scope="function")
def enumerate_service_empty():
    service = UserEnumerateService(payload_validated={})
    return service


@fixture(scope="function")
def enumerate_model():
    enumerate_model = UserEnumerateDataModel(payload_validated=stub_payload)
    return enumerate_model


@fixture(scope="function")
def enumerate_model_empty():
    enumerate_model = UserEnumerateDataModel(payload_validated={})
    return enumerate_model
