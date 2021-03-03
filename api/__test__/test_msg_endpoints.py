import pytest

from api.common.error_messages_constants import NON_EXISTANT_USER_ERROR_MSG

api_version = 1
send_msg_endpoint = f"/api/v{api_version}/message"
list_msg_endpoint = f"/api/v{api_version}/messages"

recipient_id = "002"
invalid_id = "qwerty"

# TODO mock db connection
# TODO mock endpoint with error

class TestMsgEndpoints:
    '''
    1. A short text message can be sent from one user(the sender) to another(the recipient).
    '''
    def test_send_msg_happy_path(self, client):
        res = client.post(f"{send_msg_endpoint}/{recipient_id}", json={"message": "hey bob", "sender_id": "001"})
        assert res.status_code == 201
    
    def test_msg_sent_missing_sender(self, client):
        res = client.post(f"{send_msg_endpoint}/{recipient_id}", json={"message": "hey bob"})
        assert res.status_code == 400
    
    def test_msg_sent_bad_recipient(self, client):
        res = client.post(f"{send_msg_endpoint}/{invalid_id}", json={"message": "hey bob", "sender_id": "001"})
        assert res.status_code == 400
        assert res.json["message"] == NON_EXISTANT_USER_ERROR_MSG
    
    def test_msg_sent_server_error(self, client):
        res = client.post(f"{send_msg_endpoint}/{recipient_id}", json={"message": "hey bob", "sender_id": "001"})
        assert res.status_code == 500

    '''
    2. Recent messages can be requested for a recipient from a specific sender- with a limit of 100 messages or all messages in last 30 days
    '''
    def test_request_msgs_from_specific_sender(self, client):
        res = client.post(f"{send_msg_endpoint}/{recipient_id}", json={"message": "hey bob", "sender_id": "001"})
        assert res.status_code == 200
        assert len(res.json["messages"]) <= 100 and len(res.json["messages"]) > 0
    
    def test_request_msgs_from_non_existant_recipient(self, client):
        res = client.post(f"{send_msg_endpoint}/{invalid_id}", json={"message": "hey bob", "sender_id": "001"})
        assert res.status_code == 400
        assert res.json["message"] == NON_EXISTANT_USER_ERROR_MSG
    
    def test_request_msgs_from_non_existant_sender(self, client):
        res = client.post(f"{send_msg_endpoint}/{recipient_id}", json={"message": "hey bob", "sender_id": invalid_id})
        assert res.status_code == 200
        assert len(res.json["messages"]) == 0
    
    '''
    3. Recent messages can be requested from all senders- with a limit of 100 messages or all messages in last 30 days.
    '''
    def test_request_msgs_from_all_users(self, client):
        res = client.get(list_msg_endpoint)
        assert res.status_code == 200
        assert len(res.json["messages"]) <= 100 and len(res.json["messages"]) > 0