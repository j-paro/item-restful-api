from constants import TABLE_NAMES
from db import db


class ItemModel(db.Model):
    __tablename__ = TABLE_NAMES['ItemModel']

    name = db.Column(db.String(80), primary_key=True)
    price = db.Column(db.Float(precision=2))

    store = db.Column(
        db.String(80),
        db.ForeignKey(TABLE_NAMES['StoreModel'] + '.name'),
        nullable=False
    )


    def __init__(self, name, price, store):
        self.name = name
        self.price = price
        self.store = store


    def to_json(self):
        return {
            'name': self.name,
            'price': self.price,
            'store': self.store
        }


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    #
    # This method is more applicably called "save_to_db" since those two lines
    # of code will work for both inserting and updating or "upserting" as he
    # said it's normally called.
    #
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()