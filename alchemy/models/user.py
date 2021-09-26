from constants import TABLE_NAMES
from db import db
from sqlalchemy.exc import IntegrityError


class UserExistsError(Exception):
    pass


class UserModel(db.Model):
    __tablename__ = TABLE_NAMES['UserModel']

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))

    #
    # In order for the model attributes to get saved to the database they need
    # to have the same names as the table columns.
    #
    def __init__(self, username, password):
        self.id = None
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()


    def save_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            raise UserExistsError
