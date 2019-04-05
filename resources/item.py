# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import db
from models.item import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', 
        type =  float,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('store_id', 
        type =  int,
        required = True,
        help = "Every item must have a store_id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message' : "An item with name {} already exists".format(name)}, 400
        
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        print(item)
        
        try:
            item.save_to_db()
            
        except:
            return {'message' : "An error occurred while inserting an item"}, 500 # internal server error
            
        return item, 201
    


    def delete(self, name):
        item = ItemModel.find_by_name(name)

        if item:
            item.delete_from_db()

        return {'message' : "Item deleted"}
        

    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # update_item = {'name' : name, 'price' : data['price']}
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        item.save_to_db
            # try:
            #     ItemModel.update_item(update_item)
            # except:
            #     return {'message' : "An error occurred while updating the item"}, 500
        return item.json()



class Items(Resource):
    def get(self):
        return {'item' : [item.json() for item in ItemModel.query.all()]}
        