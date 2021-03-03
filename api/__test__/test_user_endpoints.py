class TestUserEndpoints:
    api_version = 1
    users_endpoint = f"/api/v{api_version}/users"
    user_endpoint = f"/api/v{api_version}/user"

    def test_get_all_users(self, client):
        res = client.get(self.users_endpoint)
        assert res.status_code == 200
        assert len(res.json["users"]) > 0

    # maybe do a negate test where something goes wrong on our side and we have to return a 500

    def test_create_new_user(self, client):
        res = client.post(self.user_endpoint, json={"name": "Bob foobar"})
        assert res.status_code == 201
        assert res.json["id"] != None

    # maybe do a negate test where they don't provide a name and we throw a 400