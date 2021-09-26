import sqlite3

from constants import SQLITE_DB_FILE, USER_TABLE_NAME

class UserModel:

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