import sqlite3
from flask import jsonify
from db import db


class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    
    items = db.relationship('ItemModel', lazy = "dynamic")

    def __init__(self, name):
        self.name = name

    def json(self):
        return { 'id': self.id,'name': self.name}

    
    # @classmethod
    # def find_by_id(cls, id):
    #     new_store = cls.query.filter_by(id = id).first() # This is returning a StoreModel object SELECT * FROM stores WHERE id = id
    #     return new_store.json()
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name = name).first() # This is returning a StoreModel object SELECT * FROM stores WHERE name = name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
           
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()