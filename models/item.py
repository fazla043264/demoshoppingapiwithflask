import sqlite3
from db import db
from models.store import StoreModel


class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price' : self.price, 'store_id' : self.store_id}
    
    @classmethod
    def find_by_name(cls, store_name, name):
        store = StoreModel.find_by_name(store_name)

        return cls.query.filter_by(store_id = store.id, name = name).first() # This is returning a ItemModel object SELECT * FROM items WHERE name = name
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    
