from sqlalchemy.exc import IntegrityError

from constants import TABLE_NAMES
from db import db


class StoreExistsError(Exception):
    pass


class StoreModel(db.Model):
    __tablename__ = TABLE_NAMES['StoreModel']

    name = db.Column(db.String(80), primary_key=True)

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name


    def to_json(self):
        return {
            'name': self.name,
            'items': [item.to_json() for item in self.items.all()]
        }


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    
    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            raise StoreExistsError


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()