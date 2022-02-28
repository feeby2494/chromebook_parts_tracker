from enum import unique
from api import app, db, bcrypt
import jwt
import os
import datetime

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    public_id =  db.Column(db.String(50), unique=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(180), unique=False, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean(), nullable=False)

    def __init__(self, public_id, username, name, email, password, admin=False):
        self.public_id = public_id
        self.username = username
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, 10
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return f'User: name => {name} username => {username}'

    def encode_auth_token(self, public_id):
        """
            Generates the Auth Token
            :return: string
        """

        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta( hours=8 ),
                'iat': datetime.datetime.utcnow(),
                'public_id': public_id
            }

            return jwt.encode(
                payload,
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e
    
    def decode_auth_token(auth_token):
        """
            Decodes the auth token
            :param auth_token:
            :return: integer|string
        """

        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithm="HS256")
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return  'Invalid token. Please log in again.'

        


    

