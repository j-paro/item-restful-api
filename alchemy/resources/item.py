from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

#
# "flask_restful" handles making the return dictionaries into "JSON".
#
class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='The price field is required'
    )
    parser.add_argument(
        'store',
        type=str,
        required=True,
        help='The store field is required'
    )


    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        
        if item:
            return {'item': item.to_json()}, 200
        
        return {'message': 'Item not found!'}, 404


    # @jwt_required()
    def post(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel(name, **request_data)
        item.save_to_db()
        
        return {'item': item.to_json()}, 201


    # @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}, 200
        
        return {'message': 'Item not found!'}, 400


    # @jwt_required()
    def put(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            request_data = Item.parser.parse_args()
            item.price = request_data['price']
            item.store = request_data['store']
            item.save_to_db()
            return {'message': f"Item '{name}' updated."}, 200

        return self.post(name)


class ItemList(Resource):
    # @jwt_required()
    def get(self):
        item_models = ItemModel.query.all()
        items = []

        for item in item_models:
            items.append(item.to_json())

        return {'items': items}, 200