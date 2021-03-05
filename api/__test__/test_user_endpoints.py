import pytest
from api.models.user import UserModel


@pytest.fixture(autouse=True)
def mock_user_model(mocker):
    # so that we don't actually save to the db
    mocker.patch("api.models.user.UserModel.save_to_db")
    mocker.patch(
        "api.models.user.UserModel.find_all",
        return_value=[UserModel(name="john smith"), UserModel(name="mary jane")],
    )


class TestUserEndpoints:
    api_version = 1
    users_endpoint = f"/api/v{api_version}/users"
    user_endpoint = f"/api/v{api_version}/user"

    def test_get_all_users(self, client):
        res = client.get(self.users_endpoint)
        assert res.status_code == 200
        assert len(res.json["payload"]) > 0

    def test_create_new_user(self, client):
        res = client.post(self.user_endpoint, json={"name": "Bob foobar"})
        assert res.status_code == 201
        assert res.json["message"] == "successfully created user"

    def test_create_new_user_missing_name(self, client):
        res = client.post(self.user_endpoint, json={})
        assert res.status_code == 400