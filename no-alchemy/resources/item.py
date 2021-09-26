from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from constants import SQLITE_DB_FILE, ITEM_TABLE_NAME
from models.item import ItemModel, ItemExistsError

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


    @jwt_required()
    def get(self, name):
        item = ItemModel.select(name)
        
        if item:
            return {'item': item.to_json()}, 200
        
        return {'message': 'Item not found!'}, 404


    # @jwt_required()
    def post(self, name):
        request_data = Item.parser.parse_args()

        try:
            item = ItemModel(name, request_data['price'])
            item.insert()
        except ItemExistsError:
            return {'message': 'Item already exists!'}, 400
        
        return {'item': item.to_json()}, 201


    # @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete()
            return {'message': 'Item deleted.'}, 200
        
        return {'message': f"Item '{name}' doesn't exist!"}, 400


    # @jwt_required()
    def put(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            request_data = Item.parser.parse_args()
            item.update(request_data['price'])
            return {'message': f"Item '{name}' updated."}, 200

        return self.post(name)


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        item_models = ItemModel.get_all_items()
        items = []

        for item in item_models:
            items.append(item.to_json())

        return {'items': items}, 200