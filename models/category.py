import sqlite3
from flask import jsonify
from db import db
from enum import Enum
from models.user import UserModel
from flask_marshmallow import Marshmallow
from marshmallow_enum import EnumField
# from models.item import ItemSchema

# Marshmallow for JSON serialization i.e. toString() in java
ma = Marshmallow()

class Tags(Enum):
    essentials = "essentials"
    savings = "savings"
    lifestyle = "lifestyle"

class CategoryModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key = True)
    percentage = db.Column(db.Float(precision = 2), default = 0.0)
    tags = db.Column(db.Enum(Tags))
    total = db.Column(db.Float(precision = 2))
    remaining = db.Column(db.Float(precision = 2))
    items = db.relationship('ItemModel', lazy = "dynamic")

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('UserModel')

    def __init__(self, percentage, tags,  total,  remaining, user_id):
        self.percentage = percentage
        self.tags = tags
        self.total = total
        self.remaining = remaining
        self.user_id = user_id

    # def json(self):
    #     return { 'id': self.id,'name': self.name}

    
    # @classmethod
    # def find_by_id(cls, id):
    #     new_store = cls.query.filter_by(id = id).first() # This is returning a StoreModel object SELECT * FROM stores WHERE id = id
    #     return new_store.json()
    @classmethod
    def find_by_id(cls, user_id, id):
        user = UserModel.find_by_id(user_id)
        return cls.query.filter_by(user_id = user.id, id = id).first() # This is returning a StoreModel object SELECT * FROM stores WHERE name = name
    
    # @classmethod
    # def find_by_name(cls, name):
    #     return cls.query.filter_by(name = name).first() # This is returning a StoreModel object SELECT * FROM stores WHERE name = name
    
    @classmethod
    def find_by_tag(cls, tag):
        return cls.query.filter_by(tags = tag) # This is returning a StoreModel object SELECT * FROM stores WHERE tag = tag

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
           
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class CategorySchema(ma.Schema):
    tags = EnumField(Tags, by_value=True)
    class Meta:
        # Fields to expose
        # model = StoreModel
        fields = ('id','percentage','tags', 'total', 'remaining','user_id', 'links')
        #  model = StoreModel
        # item = ma.Nested(ItemSchema)

    links = ma.Hyperlinks({
        # 'self': ma.URLFor('item', store_id ='<id>', id='<id>'),
        'collection': ma.URLFor('items', category_id ='<id>')
    })
