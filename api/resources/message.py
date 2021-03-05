from flask_restful import Resource, reqparse
from api.models.message import MessageModel


class MessageList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "recipient_id",
        type=int,
        required=True,
        help="Please provide the recipient id.",
        location="json",
    )
    parser.add_argument(
        "sender_id",
        type=int,
        required=False,
        location="json",
    )

    def get(self):
        req_data = self.parser.parse_args()
        try:
            if req_data.sender_id:
                msgs = MessageModel().find_recent_from(
                    req_data.recipient_id, req_data.sender_id
                )
            else:
                # recipient id is required so this should always be safe
                msgs = MessageModel().find_recent(req_data.recipient_id)
        except:
            return {"message": "Unable to get messages"}, 500
        return {"payload": [msg.json() for msg in msgs]}


class RecipientMessages(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "sender_id",
        type=int,
        required=True,
        help="Please provide the sender_id.",
        location="json",
    )
    parser.add_argument(
        "recipient_id",
        type=int,
        required=True,
        help="Please provide the recipient_id.",
        location="json",
    )
    parser.add_argument(
        "message",
        type=str,
        required=True,
        help="Please provide a message.",
        location="json",
    )

    def post(self):
        # make sure all required fields are present
        msg_data = self.parser.parse_args()
        try:
            msg = MessageModel(**msg_data)
            msg.save_to_db()
        except:
            return {"message": "Unable to send message "}, 500
        return {"payload": msg.json()}, 201
