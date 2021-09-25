import sqlite3
from flask_restful import Resource, reqparse

from constants import SQLITE_DB_FILE, USER_TABLE_NAME

class User:

    def __init__(self, _id, username, password) -> None:
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        find_username_query = f"""
            SELECT * FROM {USER_TABLE_NAME} WHERE username=?
        """

        #
        # Query values ALWAYS have to be in the form of a tuple.
        #
        result = cursor.execute(find_username_query, (username,))
        row = result.fetchone()

        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        find_username_query = f"""
            SELECT * FROM {USER_TABLE_NAME} WHERE id=?
        """

        #
        # Query values ALWAYS have to be in the form of a tuple.
        #
        result = cursor.execute(find_username_query, (_id,))
        row = result.fetchone()

        if row:
            user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

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
