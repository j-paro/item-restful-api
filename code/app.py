from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'justin'
api = Api(app)

#
# This will implement the "/auth" route.
#
jwt = JWT(app, authenticate, identity)

items = []

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
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    # @jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None):
            return {
                'message': f"An item with name '{name}' already exists!"
            }, 400
        else:
            request_data = Item.parser.parse_args()

            item = {'name': name, 'price': request_data['price']}
            items.append(item)
            return item, 201

    # @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted.'}

    # @jwt_required()
    def put(self, name):
        request_data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item.update(request_data)
            return {
                'message': f"Item '{name}' updated."
            }, 200
        else:
            item = {'name': name, 'price': request_data['price']}
            items.append(item)
            return item, 201

class ItemList(Resource):
    # @jwt_required()
    def get(self):
        return {'items': items}

#
# This is much simpler than using Flask route decorators.
# api.add_resource(<Class Name>, <Route>)
#
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")

app.run(debug=True)