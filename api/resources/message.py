from flask_restful import Resource
from werkzeug.exceptions import InternalServerError

class MessageList(Resource):
    def get(self):
        try:
            pass
        except:
            return InternalServerError()

class RecipientMessages(Resource):
    def get(self, recipient_id):
        try:
            # add args and query db based on recipient_id
            pass
        except:
            return InternalServerError()
        return {"message": "here you go..."}

    def post(self, recipient_id):
        try:
            # send message to recipient given some sender id
            pass
        except:
            return InternalServerError()
        return {"message": "here you go..."}