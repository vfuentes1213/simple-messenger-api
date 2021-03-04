import pytest


@pytest.fixture
def mock_user_model(mocker):
    mocker.patch(
        "api.models.user.find_all", return_value=[{"name": "foo"}, {"name": "bar"}]
    )
    mocker.patch("api.models.user.save_to_db", return_value={"id": 1, "name": "bar"})


class TestUserEndpoints:
    api_version = 1
    users_endpoint = f"/api/v{api_version}/users"
    user_endpoint = f"/api/v{api_version}/user"

    def test_get_all_users(self, client):
        res = client.get(self.users_endpoint)
        assert res.status_code == 200
        assert len(res.json["users"]) > 0

    # TODO: maybe do a negate test where something goes wrong on our side and we have to return a 500

    def test_create_new_user(self, client):
        res = client.post(self.user_endpoint, json={"name": "Bob foobar"})
        assert res.status_code == 201
        assert res.json["message"] == "successfully created user"
        assert res.json["user"]["id"] != None

    def test_create_new_user_missing_name(self, client):
        res = client.post(self.user_endpoint, json={})
        assert res.status_code == 400