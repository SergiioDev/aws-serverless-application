import argon2
from marshmallow import Schema, fields, post_load, ValidationError
from argon2 import PasswordHasher

from token_utils import token
from utils import db


def encrypt(plain_text_password):
    hasher = PasswordHasher()
    hashed_password = hasher.hash(plain_text_password)
    return hashed_password


class UserSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    first_name = fields.Str(required=True)
    password = fields.Str(required=True)

    @post_load
    def encrypt_password(self, data, **kwargs):
        data["password"] = encrypt(data["password"])
        return data

    @post_load
    def validate_email(self, data, **kwargs):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection["myDB"]
            collection = database["users"]

            if collection.find_one({"email": data["email"]}) is not None:
                raise ValidationError('This email is registered')

        return data

    @post_load
    def validate_username(self, data, **kwargs):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection["myDB"]
            collection = database["users"]

            if collection.find_one({"username": data["username"]}) is not None:
                raise ValidationError('This username is registered')

        return data


class UserUpdateSchema(Schema):
    email = fields.Email(required=True)
    username = fields.Str(required=True)
    first_name = fields.Str(required=True)

    @post_load
    def encrypt_password(self, data, **kwargs):
        data["password"] = encrypt(data["password"])
        return data

    @post_load
    def validate_email(self, data, **kwargs):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection["myDB"]
            collection = database["users"]

            if collection.find_one({"email": data["email"]}) is not None:
                raise ValidationError('This email is registered')

        return data

    @post_load
    def validate_username(self, data, **kwargs):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection["myDB"]
            collection = database["users"]

            if collection.find_one({"username": data["username"]}) is not None:
                raise ValidationError('This username is registered')

        return data


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def validate_email_password(self, data, **kwargs):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['myDB']
            collection = database['users']
            result = collection.find_one({"email": data["email"]})
            if result is None:
                raise ValidationError('Sorry! You have provided invalid email.')
            else:
                ph = PasswordHasher()
                try:
                    ph.verify(result['password'], data['password'])
                    data['token'] = token.create_access_token(result)
                except argon2.exceptions.VerifyMismatchError:
                    raise ValidationError('The password is invalid.')
        return data
