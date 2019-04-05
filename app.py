import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, Items, AllItems
from resources.store import Store, StoreList

app = Flask(__name__)
app.secret_key = "random"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

# remove this before push this to staging
# this is only for creating table in the testing in the local machine
# @app.before_first_request
# def create_tables():
#     db.create_all()


jwt = JWT(app, authenticate, identity) #/auth

api.add_resource(AllItems, '/items')        
api.add_resource(Items, '/store/<string:store_name>/items')
api.add_resource(Item, '/store/<string:store_name>/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')

# api.add_resource(CitiesByNameAPI, '/api/cities/<name_or_id>', endpoint = 'cities_by_name')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run()
