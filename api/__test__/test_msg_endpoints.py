import pytest

from api.common.error_messages_constants import NON_EXISTANT_USER_ERROR_MSG
from werkzeug.exceptions import InternalServerError

# pull api version from config
api_version = 1
send_msg_endpoint = f"/api/v{api_version}/message"
list_msg_endpoint = f"/api/v{api_version}/messages"


# TODO mock db connection
# TODO format all files using precommit hook
@pytest.fixture
def mock_server_error(mocker):
    mocker.patch(
        "api.resources.message.RecipientMessages.post",
        side_effect=Exception("Something bad happened :("),
    )


class TestMsgEndpoints:
    # Test data
    RECIPIENT_ID = "002"
    INVALID_ID = "8392"
    BASIC_PAYLOAD = {"message": "hey bob", "sender_id": "001"}
    BAD_PAYLOAD = {"message": "hey bob"}

    """
    1. A short text message can be sent from one user(the sender) to another(the recipient).
    """

    def test_send_msg_happy_path(self, client):
        res = client.post(
            f"{send_msg_endpoint}/{self.RECIPIENT_ID}", json=self.BASIC_PAYLOAD
        )
        assert res.status_code == 201

    def test_send_msg_missing_sender(self, client):
        res = client.post(
            f"{send_msg_endpoint}/{self.RECIPIENT_ID}", json={"message": "hey bob"}
        )
        assert res.status_code == 400

    def test_send_msg_bad_recipient(self, client):
        res = client.post(
            f"{send_msg_endpoint}/{self.INVALID_ID}", json=self.BAD_PAYLOAD
        )
        assert res.status_code == 400
        assert res.json["message"] == NON_EXISTANT_USER_ERROR_MSG

    # @pytest.mark.usefixtures("mock_server_error")
    # def test_send_msg_server_error(self, client):
    #     res = client.post(
    #         f"{send_msg_endpoint}/{self.RECIPIENT_ID}", json=self.BASIC_PAYLOAD
    #     )
    #     assert res.status_code == 500

    """
    2. Recent messages can be requested for a recipient from a specific sender- with a limit of 100 messages or all messages in last 30 days
    """

    def test_get_msgs_from_specific_sender(self, client):
        res = client.get(
            f"{send_msg_endpoint}/{self.RECIPIENT_ID}",
            json={"message": "hey bob", "sender_id": "001"},
        )
        assert res.status_code == 200
        assert len(res.json["messages"]) <= 100 and len(res.json["messages"]) > 0

    def test_get_msgs_from_non_existant_recipient(self, client):
        res = client.get(
            f"{send_msg_endpoint}/{self.INVALID_ID}",
            json={"message": "hey bob", "sender_id": "001"},
        )
        assert res.status_code == 400
        assert res.json["message"] == NON_EXISTANT_USER_ERROR_MSG

    def test_get_msgs_from_non_existant_sender(self, client):
        res = client.get(
            f"{send_msg_endpoint}/{self.RECIPIENT_ID}",
            json={"message": "hey bob", "sender_id": self.INVALID_ID},
        )
        assert res.status_code == 200
        assert len(res.json["messages"]) == 0

    """
    3. Recent messages can be requested from all senders- with a limit of 100 messages or all messages in last 30 days.
    """

    def test_get_msgs_from_all_recipients(self, client):
        res = client.get(list_msg_endpoint)
        assert res.status_code == 200
        assert len(res.json["messages"]) <= 100 and len(res.json["messages"]) > 0