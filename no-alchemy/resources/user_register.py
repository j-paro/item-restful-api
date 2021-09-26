import sqlite3
from flask_restful import Resource, reqparse

from constants import SQLITE_DB_FILE, USER_TABLE_NAME

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='This field is required!'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='This field is required!'
    )

    def post(self):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        request_data = UserRegister.parser.parse_args()

        register_user_query = f"""
            INSERT INTO {USER_TABLE_NAME} VALUES (NULL, ?, ?)
        """
        try:
            cursor.execute(
                register_user_query,
                (
                    request_data['username'],
                    request_data['password']
                )
            )
        except sqlite3.IntegrityError:
            connection.close()
            return {'message': 'User already exists!'}, 400
        else: 
            connection.commit()
            return {'message': 'User created successfully!'}, 201
