from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemList

app = Flask(__name__)
app.secret_key = 'justin'
api = Api(app)

#
# This will implement the "/auth" route.
#
jwt = JWT(app, authenticate, identity)

#
# This is much simpler than using Flask route decorators.
# api.add_resource(<Class Name>, <Route>)
#
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if __name__ == '__main__':
    app.run(debug=True)