from api.resources.message import MessageList, RecipientMessages
from api.resources.user import UserList, User


def initialize_routes(api):
    api.add_resource(RecipientMessages, "/message")
    api.add_resource(MessageList, "/messages")
    api.add_resource(User, "/user")
    api.add_resource(UserList, "/users")
