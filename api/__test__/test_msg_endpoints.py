import pytest

api_version = 1
endpoint = f"/api/v{api_version}/message"

class TestMsgEndpoints:
    '''
    1. A short text message can be sent from one user(the sender) to another(the recipient).
    '''
    def test_send_msg_happy_path(self, client):
        pass
    
    def test_msg_sent_missing_recipient(self, client):
        pass
    
    def test_msg_sent_server_error(self, client):
        pass

    '''
    2. Recent messages can be requested for a recipient from a specific sender- with a limit of 100 messages or all messages inlast 30 days
    '''
    def test_request_msgs_from_specific_user(self, client):
        pass
    
    def test_request_msgs_from_non_existant_user(self, client):
        pass
    
    '''
    3. Recent messages can be requested from all senders- with a limit of 100 messages or all messages in last 30 days.
    '''
    def test_request_msgs_from_all_users(self, client):
        pass