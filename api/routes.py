from api.resources.message import MessageList, RecipientMessages

def initialize_routes(api):
    api.add_resource(RecipientMessages, "/message/<int:recipient_id>")
    api.add_resource(MessageList, "/messages")