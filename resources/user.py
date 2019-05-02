import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel, UserSchema
from flask_bcrypt import check_password_hash, generate_password_hash
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)   

user_schema = UserSchema()
users_schema = UserSchema(many=True)

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('lastname', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('salary', 
        type =  float,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('email', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('password', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {"message": "User with this email address already exist"}, 400
        
        
        data['admin'] = False
        user = UserModel(**data)
        # user.save_to_db()

        # return {"message": "User created successfully."}, 201



        
        try:
            user.save_to_db()
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'User {} was created successfully'.format(data['email']),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 201
        except:
            return {'message': 'Something went wrong'}, 500


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('password', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if not user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}
        
        if check_password_hash(user.password, data['password']):
            access_token = create_access_token(identity = data['email'])
            refresh_token = create_refresh_token(identity = data['email'])
            return {
                'message': 'Logged in as {}'.format(user.email),
                'access_token': access_token,
                'refresh_token': refresh_token
                }
        else:
            return {'message': 'Wrong credentials'}, 403


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}

# from werkzeug.security import safe_str_cmp
# from models.user import UserModel
# from flask_bcrypt import check_password_hash


# def authenticate(username, password):
#     user = UserModel.find_by_username(username)
#     if user and check_password_hash(user.password, password):
#         return user


# def identity(payload):
#     user_id = payload['identity']
#     return UserModel.find_by_id(user_id)

# class UserIdentity(Resource):
#     @jwt_required
#     def get(self):
#         email = get_jwt_identity()
#         return ({'hello': 'from {}'.format(email)}), 200




class User(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('firstname', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('lastname', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('salary', 
        type =  float,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('email', 
        type =  str,
        required = True,
        help = "this field can't be left blank!"
    )
    parser.add_argument('password', 
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
    def get(self):
        email = get_jwt_identity()
        user = UserModel.find_by_email(email)        
        if user:
            return user_schema.dump(user).data
        return {"message" : "user not found"}, 404
    
    @jwt_required
    def put(self):
        
        email = get_jwt_identity()
        user = UserModel.find_by_email(email)
        data = User.parser.parse_args()
        # data['id'] = user.id
        
        # sum = db.session.query(func.sum(CategoryModel.percentage)).scalar()
        # if user:
        #     user = UserModel(**data)
        #     print(user.id)
        if user:
            user.firstname = data['firstname']
            user.lastname = data['lastname']
            user.salary = data['salary']
            user.email = data['email']
            user.password = generate_password_hash(data['password']).decode('utf-8')
            user.admin = False

        user.save_to_db()
            # try:
            #     ItemModel.update_item(update_item)
            # except:
            #     return {'message' : "An error occurred while updating the item"}, 500
        return user_schema.dump(user).data, 201
    @jwt_required
    def delete(self):
        email = get_jwt_identity()
        user = UserModel.find_by_email(email)
        
        if user:
            user.delete_from_db()
        
        return {"message" : "user of name {} deleted".format(user.firstname)}




class UserList(Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        # print(email)
        user = UserModel.find_by_email(email)
        # print(user.id)
        #  print(user.stores)
        if user.admin: 
            users = UserModel.query.all()
            if users:
                return users_schema.dump(users).data
        return {"message" : "Forbidden"}, 403

class UserToAdmin(Resource):
    @jwt_required
    def put(self):
        email = get_jwt_identity()
        user = UserModel.find_by_email(email)
        if user:
            user.admin = True

        user.save_to_db()
        return user_schema.dump(user).data, 201
    