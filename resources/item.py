# import sqlite3
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from flask_jwt_extended import jwt_required
from db import db
from datetime import datetime
from sqlalchemy import func
from models.category import CategoryModel
from models.item import ItemModel, ItemSchema
from models.user import UserModel
from flask_jwt_extended import jwt_required, get_jwt_identity
# import datetime
# Explicitly kick off the background thread

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('amount', 
        type =  float,
        required = True,
        help = "this field can't be left blank!"
    )
    # parser.add_argument('category_id', 
    #     type =  int,
    #     required = True,
    #     help = "Every item must have a category_id!"
    # )
    @jwt_required
    def get(self, category_id, id):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        # category = CategoryModel.find_by_id(user.id, id)
        item = ItemModel.find_by_id(current_user.id, category_id, id)
        # print(item)
        if item:
            return item_schema.dump(item).data
        return {'message': "Item not found"}, 404

    @jwt_required
    def post(self, category_id):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        # if ItemModel.find_by_id(category_id, id):
        #     return {'message' : "An item with id {} already exists".format(id)}, 400
        
        data = Item.parser.parse_args()
        category = CategoryModel.find_by_id(current_user.id,category_id)
        data['category_id'] = category.id
        # data['date'] = datetime.now()
        sum = db.session.query(func.sum(ItemModel.amount)).filter(ItemModel.category_id == category.id).scalar()
        print(sum)
        if sum == None and data['amount'] <= category.total: 
            item = ItemModel(**data)
            category.remaining = category.total - data['amount']
        elif sum!= None and data['amount'] + sum <= category.total:
        # print(item)
            item = ItemModel(**data)
            category.remaining = category.total - (data['amount'] + sum)
        else:
            if sum!= None and data['amount'] + sum >= category.total:
                return {'message' : "amount can't be more than {}".format(category.remaining)}, 400        
            else:
                return {'message' : "something wrong happended while saving {} item".format(data['name'])}, 500
        
        try:
            item.save_to_db()
            
        except:
            return {'message' : "An error occurred while inserting an item"}, 500 # internal server error
            
        return item_schema.dump(item).data, 201
    

    @jwt_required
    def delete(self, category_id, id):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        category = CategoryModel.find_by_id(current_user.id, category_id)
        item = ItemModel.find_by_id(current_user.id, category_id, id)
        # print(email)
        # item = ItemModel.find_by_id(current_user.id, category_id, id)
        print(category)
        if item:
            category.remaining += item.amount
            item.delete_from_db()
            return {'message' : "Item {} deleted".format(item.name)}, 200 
        elif not category:
            return { 'message' : "Category not found" }
        else:
            return {"message" : "Item not found"}, 404
        
    @jwt_required
    def put(self,category_id, id):
        data = Item.parser.parse_args()
        
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        category = CategoryModel.find_by_id(current_user.id ,category_id)
        item = ItemModel.find_by_id(current_user.id, category_id, id)
        data['category_id'] = category.id
        # data['date'] = datetime.now()
        sum = db.session.query(func.sum(ItemModel.amount)).filter(ItemModel.category_id == category.id).scalar()
        # update_item = {'name' : name, 'price' : data['price']}
        if item is None:
            if sum == None and data['amount'] <= category.total: 
                item = ItemModel(**data)
                category.remaining = category.total - data['amount']
            elif sum!= None and data['amount'] + sum <= category.total:
            # print(item)
                item = ItemModel(**data)
                category.remaining = category.total - (data['amount'] + sum)
            else:
                if sum!= None and data['amount'] + sum >= category.total:
                    return {'message' : "amount can't be more than {}".format(category.remaining)}, 400        
                else:
                    return {'message' : "something wrong happended while saving {} item".format(data['name'])}, 500
        else:
            current_item_amount = item.amount
            item.name = data['name']
            item.amount = data['amount']
            category.remaining = category.remaining + (current_item_amount - data['amount'])
            # item.category_id = category.id
            
        item.save_to_db()
            # try:
            #     ItemModel.update_item(update_item)
            # except:
            #     return {'message' : "An error occurred while updating the item"}, 500
        return item_schema.dump(item).data, 201



class Items(Resource):
    @jwt_required
    def get(self,category_id):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        category = CategoryModel.find_by_id( current_user.id, category_id)
        results = items_schema.dump(category.items)
        # return {'items' : [item.json() for item in category.items]}
        return results.data

class AllItems(Resource):
    def get(self):
        return {'Items' : [item_schema.dump(item).data for item in ItemModel.query.all()]}
    
        