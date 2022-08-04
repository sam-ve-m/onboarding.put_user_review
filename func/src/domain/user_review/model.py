class UserReviewModel:
    def __init__(self, user_review_data_validated: dict, unique_id: str, modified_register_data: dict):
        self.user_review_data = user_review_data_validated
        self.unique_id = unique_id
        self.modified_register_data = modified_register_data

    async def get_audit_template(self):
        audit_template = {
            "unique_id": self.unique_id,
            "modified_register_data": self.modified_register_data,
            "update_customer_registration_data": self.user_review_data,
        }
        return audit_template
