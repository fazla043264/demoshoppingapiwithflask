import sqlite3
from db import db
from flask_bcrypt import generate_password_hash

class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password): 
        self.username = username
        self.password = generate_password_hash(
            password)
    
    def save_to_db(self):

        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()
        # connection = sqlite3.connect("data.db")
        # curser = connection.cursor()

        # query = "SELECT * FROM users WHERE username = ?"
        # result = curser.execute(query,(username,))
        # row = result.fetchone()

        # if row:
        #     user = cls(*row) 
        #     #  same as creating an User object, i.e. User(row[0], row[1], row[2]) 
        # else:
        #     user = None

        # # no need to commit as we didn't insert any data 
        # connection.close()
        # return user

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id = _id).first()
        # connection = sqlite3.connect("data.db")
        # curser = connection.cursor()

        # query = "SELECT * FROM users WHERE id = ?"
        # result = curser.execute(query,(_id,))
        # row = result.fetchone()

        # if row:
        #     user = cls(*row) 
        #     #  same as creating an User object, i.e. User(row[0], row[1], row[2]) 
        # else:
        #     user = None
        
        # # no need to commit as we didn't insert any data 
        # connection.close()
        # return user 