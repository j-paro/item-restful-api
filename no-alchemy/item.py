import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from constants import SQLITE_DB_FILE, ITEM_TABLE_NAME

#
# "flask_restful" handles making the return dictionaries into "JSON".
#
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field is required!'
    )


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        query = f"SELECT * FROM {ITEM_TABLE_NAME} WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    @jwt_required()
    def get(self, name):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        get_item_query = f"""
            SELECT * FROM {ITEM_TABLE_NAME} WHERE name=?
        """
        print(name)
        result = cursor.execute(get_item_query, (name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}, 200
        
        return {'message': 'Item not found!'}, 404


    # @jwt_required()
    def post(self, name):
        request_data = Item.parser.parse_args()

        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        try:
            insert_item_query = f"""
                INSERT INTO {ITEM_TABLE_NAME} VALUES(?, ?)
            """
            cursor.execute(insert_item_query, (name, request_data['price']))
        except sqlite3.IntegrityError as e:
            connection.close()
            print(e.__str__())
            print(e.__repr__())
            return {'message': 'Item already exists!'}, 400
        else:
            connection.commit()
            connection.close()
            return {'item': {'name': name, 'price': request_data['price']}}, 201


    # @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        delete_item_query = f"""
            DELETE FROM {ITEM_TABLE_NAME} WHERE name=?
        """
        cursor.execute(delete_item_query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted.'}


    # @jwt_required()
    def put(self, name):
        item = Item.find_by_name(name)

        if item:
            request_data = Item.parser.parse_args()
            
            connection = sqlite3.connect(SQLITE_DB_FILE)
            cursor = connection.cursor()

            item_modify_query = f"""
                UPDATE {ITEM_TABLE_NAME}
                SET price=?
                WHERE name=?
            """
            cursor.execute(item_modify_query, (request_data['price'], name))

            connection.commit()
            connection.close()

            return {'message': f"Item '{name}' updated."}, 200
        else:
            return self.post(name)


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        connection = sqlite3.connect(SQLITE_DB_FILE)
        cursor = connection.cursor()

        get_items_query = f"""
            SELECT * FROM {ITEM_TABLE_NAME}
        """
        result = cursor.execute(get_items_query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.commit()
        connection.close()

        return {'items': items}