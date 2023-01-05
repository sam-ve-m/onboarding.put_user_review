import pytest
from unittest.mock import patch, call
from func.src.repositories.mongo_db.user.repository import UserRepository

dummy_unique_id = "unique_id"
dummy_update = {}


@pytest.mark.asyncio
@patch.object(UserRepository, "_get_collection")
async def test_update_one_with_user_review_data(mocked_collection):
    result = await UserRepository.update_one_with_user_review_data(
        dummy_unique_id, dummy_update
    )
    mocked_collection.return_value.update_one.assert_has_calls(
        (
            call({"unique_id": dummy_unique_id}, {"$set": dummy_update}),
            call(
                {"unique_id": dummy_unique_id},
                {"$set": {"is_bureau_data_validated": True}},
            ),
        )
    )
    assert mocked_collection.return_value.update_one.return_value
