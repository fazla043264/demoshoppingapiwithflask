from flask_restful import Resource, reqparse
from models.category import CategoryModel, CategorySchema
from models.user import UserModel
from db import db
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)

class Category(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('percentage', 
        type =  float,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('tags', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    # parser.add_argument('user_id', 
    #     type =  int,
    #     required = True,
    #     help = "Every item must have a user_id!"
    # )
    @jwt_required
    def get(self, id):
        email = get_jwt_identity()
        user = UserModel.find_by_email(email)
        category = CategoryModel.find_by_id(user.id, id)
        if category:
            return category_schema.dump(category).data
        return {"message" : "Category not found"}, 404
    @jwt_required
    def post(self):
        email = get_jwt_identity()
        current_user = UserModel.find_by_email(email)
        
        data = Category.parser.parse_args()
        data['user_id'] = current_user.id
        total_per_category = (data['percentage'] / 100) * current_user.salary
        data['total'] = total_per_category
        data['remaining'] = total_per_category
        # data['remaining'] = total_per_category - 
        sum = db.session.query(func.sum(CategoryModel.percentage)).scalar()
        # number_of_tags = db.session.query(func.count(StoreModel.id)).scalar()

        # print(number_of_tags)


        if sum == None and data['percentage'] <= 100:
            category = CategoryModel(**data)
            
            
        elif sum!= None and data['percentage'] + sum <= 100 and not db.session.query(CategoryModel.tags).filter_by(tags = data['tags']).all():
            category = CategoryModel(**data)
            
        else:
            if not (sum!= None and data['percentage'] + sum <= 100):
                return {'message' : "total percentage can't be more than 100%"}, 400
            elif db.session.query(CategoryModel.tags).filter_by(tags = data['tags']).all():
                return {'message' : "you have already used this {} tag. One tag can be used only once but can be edited".format(data['tags'])}, 403        
            else:
                return {'message' : "You are not allowed to add more than 3 tags"}, 400
        try:
            category.save_to_db()
            
        except:
            return {'message' : "An error occurred while inserting an item"}, 500 # internal server error
            
        return category_schema.dump(category).data, 201

    @jwt_required
    def put(self, id):
        
        email = get_jwt_identity()
        data = Category.parser.parse_args()
        user = UserModel.find_by_email(email)
        category = CategoryModel.find_by_id(user.id, id)
        data['user_id'] = user.id
        
        sum = db.session.query(func.sum(CategoryModel.percentage)).scalar()
        if category is None:
            

            if sum == None and data['percentage'] <= 100:
                category = CategoryModel(**data)
                
            elif sum!= None and data['percentage'] + sum <= 100 and not db.session.query(CategoryModel.tags).filter_by(tags = data['tags']).all():
                category = CategoryModel(**data)
                
            else:
                if not (sum!= None and data['percentage'] + sum <= 100):
                    return {'message' : "total percentage can't be more than 100%"}, 400
                elif db.session.query(CategoryModel.tags).filter_by(tags = data['tags']).all():
                    return {'message' : "you have already used this {} tag. One tag can be used only once but can be edited".format(data['tags'])}, 400        
                else:
                    return {'message' : "You are not allowed to add more than 3 tags"}, 400
        elif sum!= None and (data['percentage'] + sum) - db.session.query(CategoryModel.percentage).filter_by(tags = data['tags']).scalar() <= 100:
            
            category.percentage = data['percentage']
        else:
            return {'message' : "total percentage can't be more than 100%"}, 400

        category.save_to_db()
            # try:
            #     ItemModel.update_item(update_item)
            # except:
            #     return {'message' : "An error occurred while updating the item"}, 500
        return category_schema.dump(category).data, 201
    @jwt_required
    def delete(self, id):
        email = get_jwt_identity()
        user = UserModel.find_by_email(email)
        category = CategoryModel.find_by_id(user.id, id)
        if category:
            category.delete_from_db()
        
        return {"message" : "category deleted"}


class CategoryList(Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        # print(email)
        user = UserModel.find_by_email(email)
        # print(user.id)
        #  print(user.stores)
        results = categories_schema.dump(user.categories)
        # print(results)
        
        return results.data
       

class CategoryByTags(Resource):
    def get(self, tag):
        categories = CategoryModel.find_by_tag(tag)
        
        if categories:
            return categories_schema.dump(categories).data
        return {"message" : "Categories not found"}, 404