import os
import datetime
from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager
from datetime import date
# from security import authenticate, identity
from resources.user import UserRegister, UserLogin, TokenRefresh, User, UserList, UserToAdmin, UserLogoutAccess, UserLogoutRefresh #UserIdentity
from resources.item import Item, Items, AllItems
from models.user import RevokedTokenModel
from models.item import ItemModel
from models.category import CategoryModel
from resources.category import Category, CategoryList, CategoryByTags
from apscheduler.schedulers.background import BackgroundScheduler



app = Flask(__name__)
# app.secret_key = "random"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
CORS(app)


# flask_jwt_extended JWT_SECRET_KEY 
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'super-secret')
# JWT access token will expire after 60 minutes
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(minutes = 60)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']




# remove this before push this to staging
# this is only for creating table in the testing in the local machine
# @app.before_first_request
# def create_tables():
#     db.create_all()

# flask_jwt
# jwt = JWT(app, authenticate, identity) #/auth
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return RevokedTokenModel.is_jti_blacklisted(jti)



def sensor():
    with app.app_context():
        today = date.today()
        month_start = today.replace(day=1)
        # print(month_start)
        items = ItemModel.query.filter(ItemModel.date < month_start).all()
        if items:
            for item in items:
                print("{} item deleted".format(item.name))
                item.delete_from_db()
                CategoryModel.query.update({CategoryModel.remaining: CategoryModel.total}) 
        # db.session.flush()
        # db.session.commit()
        # print("Scheduler is alive!")

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',hours=12)
sched.start()



# all the resources
api.add_resource(AllItems, '/items')        
api.add_resource(Items, '/category/<category_id>/items')
api.add_resource(Item, '/category/<category_id>/item','/category/<category_id>/item/<id>')
api.add_resource(Category, '/category','/category/<id>')
api.add_resource(CategoryList, '/categories')
api.add_resource(CategoryByTags, '/categories/<string:tag>')
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/auth')
api.add_resource(User,'/user')
api.add_resource(UserList,'/allusers')
api.add_resource(UserLogoutAccess, '/logout/access')
api.add_resource(UserLogoutRefresh, '/logout/refresh')
# api.add_resource(UserToAdmin, '/admin/register')
# api.add_resource(UserIdentity, '/user/identity')

api.add_resource(TokenRefresh, '/token/refresh')


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run()
