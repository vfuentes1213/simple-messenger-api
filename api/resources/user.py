from flask_restful import Resource, reqparse
from werkzeug.exceptions import InternalServerError
from api.models.user import UserModel


class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "name",
        type=str,
        required=True,
        help="Please provide the name of the user.",
        location="json",
    )

    def post(self):
        # make sure all required fields are present
        user_data = self.parser.parse_args()

        try:
            user = UserModel(**user_data)
            user.save_to_db()
        except Exception:
            return {"message": "Unable to create user"}, 500
        return {"message": "successfully created user", "user": user.json()}, 201


class UserList(Resource):
    def get(self):
        return {"users": [user.json() for user in UserModel.find_all()]}
