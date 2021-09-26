from flask_restful import Resource
from models.store import StoreModel, StoreExistsError


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.to_json()

        return {'message': 'Store not found'}, 404

    def post(self, name):
        store = StoreModel(name)
        try:
            store.save_to_db()
        except StoreExistsError:
            return {'message': 'This store already exists!'}, 400

        return store.to_json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {'message': 'Store deleted.'}

        return {'message': 'Store does not exist!'}


class StoreList(Resource):
    def get(self):
        return {
            'stores': list(
                map(
                    lambda x: x.to_json(), StoreModel.query.all()
                )
            )
        }