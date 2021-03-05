import pytest

from api.models.message import MessageModel


@pytest.fixture
def mock_server_error(mocker):
    mocker.patch(
        "api.models.message.MessageModel.save_to_db",
        side_effect=Exception("Something bad happened :("),
    )


@pytest.fixture(autouse=True)
def mock_message_model(mocker):
    # so that we don't actually save to the db
    mocker.patch("api.models.message.MessageModel.save_to_db")


@pytest.fixture()
def mock_get_from_all_senders(mocker):
    mocker.patch(
        "api.models.message.MessageModel.find_recent",
        return_value=[
            MessageModel(recipient_id=1, sender_id=2, message="hello world"),
            MessageModel(recipient_id=1, sender_id=3, message="hello world"),
            MessageModel(recipient_id=1, sender_id=4, message="hello world"),
        ],
    )


@pytest.fixture()
def mock_get_from_specific_sender(mocker):
    mocker.patch(
        "api.models.message.MessageModel.find_recent_from",
        return_value=[
            MessageModel(recipient_id=1, sender_id=2, message="hello world"),
            MessageModel(recipient_id=1, sender_id=2, message="hello world"),
            MessageModel(recipient_id=1, sender_id=2, message="hello world"),
        ],
    )


class TestMsgEndpoints:
    # Test data
    RECIPIENT_ID = 1
    SEND_MSG_GOOD_PAYLOAD = {"message": "hey bob", "sender_id": 1, "recipient_id": 2}
    SEND_MSG_BAD_PAYLOAD = {"message": "hey bob"}
    GET_MSG_GOOD_PAYLOAD = {"message": "hey bob", "sender_id": 1, "recipient_id": 2}
    GET_MSG_GOOD_PAYLOAD_ALL = {"message": "hey bob", "recipient_id": 2}

    API_VERSION = 1
    SEND_MSG_ENDPOINT = f"/api/v{API_VERSION}/message"
    LIST_MSG_ENDPOINT = f"/api/v{API_VERSION}/messages"

    """
    1. A short text message can be sent from one user(the sender) to another(the recipient).
    """

    def test_send_msg_happy_path(self, client):
        res = client.post(
            self.SEND_MSG_ENDPOINT,
            json=self.SEND_MSG_GOOD_PAYLOAD,
        )
        assert res.status_code == 201

    def test_send_msg_missing_sender(self, client):
        res = client.post(self.SEND_MSG_ENDPOINT, json={"message": "hey bob"})
        assert res.status_code == 400

    @pytest.mark.usefixtures("mock_server_error")
    def test_send_msg_server_error(self, client):
        res = client.post(
            self.SEND_MSG_ENDPOINT,
            json=self.SEND_MSG_GOOD_PAYLOAD,
        )
        assert res.status_code == 500

    """
    2. Recent messages can be requested for a recipient from a specific sender- with a limit of 100 messages or all messages in last 30 days
    """

    @pytest.mark.usefixtures("mock_get_from_specific_sender")
    def test_get_recent_msgs_from_specific_sender(self, client):
        res = client.get(
            f"{self.LIST_MSG_ENDPOINT}",
            json=self.GET_MSG_GOOD_PAYLOAD,
        )
        assert res.status_code == 200
        assert len(res.json["payload"]) <= 100 and len(res.json["payload"]) > 0

    """
    3. Recent messages can be requested from all senders- with a limit of 100 messages or all messages in last 30 days.
    """

    @pytest.mark.usefixtures("mock_get_from_all_senders")
    def test_get_msgs_from_all_senders(self, client):
        res = client.get(self.LIST_MSG_ENDPOINT, json=self.GET_MSG_GOOD_PAYLOAD_ALL)
        assert res.status_code == 200
        assert len(res.json["payload"]) <= 100 and len(res.json["payload"]) > 0
