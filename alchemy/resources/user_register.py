from flask_restful import Resource, reqparse

from models.user import UserModel, UserExistsError

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='Username is required!'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='Password is required!'
    )

    def post(self):
        request_data = UserRegister.parser.parse_args()

        user = UserModel(**request_data)

        try:
            user.save_to_db()
            return {'message': f"User '{user.username}' created."}, 201
        except UserExistsError:
            return {'message': 'This user already exists!'}, 400
