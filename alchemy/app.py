from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user_register import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db
from constants import DATABASE

app = Flask(__name__)
#
# The following turns off the Flask-SQLAlchemy tracker but not the regular
# SQLAlchemy tracker.
#
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'justin'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

#
# This will implement the "/auth" route. It's "/auth" by default.
#
jwt = JWT(app, authenticate, identity)

#
# This is much simpler than using Flask route decorators.
# api.add_resource(<Class Name>, <Route>)
#
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)