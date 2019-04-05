# import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db import db
from models.store import StoreModel
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
    def get(self, store_name, name):
        item = ItemModel.find_by_name(store_name, name)
        if item:
            return item.json()
        return {'message': "Item not found"}, 404

    def post(self, store_name, name):
        if ItemModel.find_by_name(store_name, name):
            return {'message' : "An item with name {} already exists".format(name)}, 400
        
        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        print(item)
        
        try:
            item.save_to_db()
            
        except:
            return {'message' : "An error occurred while inserting an item"}, 500 # internal server error
            
        return item.json(), 201
    


    def delete(self, store_name, name):
        item = ItemModel.find_by_name(store_name, name)

        if item:
            item.delete_from_db()

        return {'message' : "Item deleted"}
        

    def put(self,store_name, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(store_name, name)
        store = StoreModel.find_by_name(store_name)
        # update_item = {'name' : name, 'price' : data['price']}
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = store.id
            print("store.id = ", store.id )
            print("item.store_id = ", item.store_id)
            print(item)
        item.save_to_db()
            # try:
            #     ItemModel.update_item(update_item)
            # except:
            #     return {'message' : "An error occurred while updating the item"}, 500
        return item.json(), 201



class Items(Resource):
    def get(self,store_name):
        store = StoreModel.find_by_name(store_name)

        return {'items' : [item.json() for item in store.items]}

class AllItems(Resource):
    def get(self):
        return {'Items' : [item.json() for item in ItemModel.query.all()]}
        