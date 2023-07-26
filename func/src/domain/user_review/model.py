from typing import Optional

from regis import RegisResponse

from .validator import UserReviewData
from ..models.device_info import DeviceInfo


class UserReviewModel:
    def __init__(
        self,
        user_review_data: dict,
        unique_id: str,
        modified_register_data: dict,
        new_user_registration_data: dict,
        device_info: Optional[DeviceInfo],
        risk_data: RegisResponse = None,
    ):
        self.user_review_data = user_review_data
        self.unique_id = unique_id
        self.modified_register_data = modified_register_data
        self.new_user_registration_data = new_user_registration_data
        self.device_info = device_info
        self.risk_data = risk_data

    def add_risk_data(self, risk_data: RegisResponse):
        self.risk_data = risk_data

    def update_new_data_with_risk_data(self):
        risk_data_template = {
            "pld": {
                "rating": self.risk_data.risk_rating.value,
                "score": self.risk_data.risk_score,
            }
        }
        self.new_user_registration_data.update(risk_data_template)

    def update_new_data_with_expiration_dates(self):
        expiration_dates_template = {
            "record_date_control": {"current_pld_risk_rating_defined_in": self.risk_data.expiration_date},
            "expiration_dates": {
                "suitability": self.risk_data.expiration_date,
                "register": self.risk_data.expiration_date,
            }
        }
        self.new_user_registration_data.update(expiration_dates_template)

    async def get_audit_template_to_update_registration_data(self) -> dict:
        audit_template = {
            "unique_id": self.unique_id,
            "modified_register_data": self.modified_register_data,
            "update_customer_registration_data": self.user_review_data,
        }
        if self.device_info:
            audit_template.update({
                "device_info": self.device_info.device_info,
                "device_id": self.device_info.device_id
            })
        return audit_template

    async def get_audit_template_to_update_risk_data(self) -> dict:
        audit_template = {
            "unique_id": self.unique_id,
            "score": self.risk_data.risk_score,
            "rating": self.risk_data.risk_rating.value,
            "approval": self.risk_data.risk_approval,
            "validations": self.risk_data.risk_validations.to_dict(),
        }
        if self.device_info:
            audit_template.update({
                "device_info": self.device_info.device_info,
                "device_id": self.device_info.device_id
            })
        if not audit_template["approval"]:
            audit_template.update({"user_data": self.new_user_registration_data})
        return audit_template

    async def get_new_user_data(self) -> dict:
        del self.new_user_registration_data["_id"]
        return self.new_user_registration_data

    async def get_iara_message_template(self) -> dict:
        message = {
            "unique_id": self.unique_id,
        }
        return message
