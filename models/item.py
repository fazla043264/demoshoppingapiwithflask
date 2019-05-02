import sqlite3
# import atexit
from db import db
from datetime import datetime, date
from models.category import CategoryModel, CategorySchema
from flask_marshmallow import Marshmallow



# Marshmallow for JSON serialization i.e. toString() in java
ma = Marshmallow()

  # set day of the month to 1

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    amount = db.Column(db.Float(precision = 2))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    # total = db.Column(db.Float(precision = 2))
    # remaining = db.Column(db.Float(precision = 2))

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    category = db.relationship('CategoryModel')

    def __init__(self, name, amount, category_id):
        self.name = name
        self.amount = amount
        # self.date = date
        self.category_id = category_id

    # def json(self):
    #     return {'name': self.name, 'price' : self.price, 'store_id' : self.store_id}
    
    @classmethod
    def find_by_id(cls, user_id, category_id, id):
        # user = UserModel.find_by_id(user_id)
        category = CategoryModel.find_by_id(user_id, category_id)

        return cls.query.filter_by(category_id = category.id, id = id).first() # This is returning a ItemModel object SELECT * FROM items WHERE name = name
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    # @classmethod
    # def delete_expired_items_from_db(cls):
    #     cls.query.filter(cls.date <= month_start).delete()
    #     db.session.commit()
    # @cron.interval_schedule(hours=1)
    # def delete_all_from_db(self):
    #     self.query.filter(self.date < month_start).delete()
    #     db.session.commit()
    
    #  result = category_schema.dump(category).data
class ItemSchema(ma.ModelSchema):
    class Meta:
        # Fields to expose
        model = ItemModel

    category = ma.HyperlinkRelated("category")

    #     fields = ('id','name','price','store')
    # store = ma.Nested(StoreSchema)

    # links = ma.Hyperlinks({
    #     'self': ma.URLFor('item_detail', id='<id>'),
    #     'collection': ma.URLFor('item_list')
    # })
