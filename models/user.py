import sqlite3
from db import db
from flask_bcrypt import generate_password_hash
from flask_marshmallow import Marshmallow


ma = Marshmallow()
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    firstname = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    salary = db.Column(db.Float(precision = 2))
    email = db.Column(db.String(255))
    password = db.Column(db.String())
    admin = db.Column(db.Boolean, default= False)
    categories = db.relationship('CategoryModel', lazy = "dynamic")

    def __init__(self, firstname, lastname, salary, email, password, admin):
        self.firstname = firstname
        self.lastname = lastname
        self.salary = salary 
        self.email = email
        self.password = generate_password_hash(password).decode('utf-8')
        self.admin = admin
    
    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()


    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
      
class UserSchema(ma.Schema):
    # tags = EnumField(Tags, by_value=True)
    class Meta:
        # Fields to expose
        # model = StoreModel
        fields = ('id','firstname','lastname', 'salary','email', 'password', 'links', 'admin')
        #  model = StoreModel
        # item = ma.Nested(ItemSchema)

    links = ma.Hyperlinks({
        # 'self': ma.URLFor('item', store_id ='<id>', id='<id>'),
        'collection': ma.URLFor('categorylist', user_id ='<id>')
    })