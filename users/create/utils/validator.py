from marshmallow import Schema, fields, post_load, ValidationError
from argon2 import PasswordHasher
from utils import db


def encrypt(plain_text_password):
    hasher = PasswordHasher()
    hashed_password = hasher.hash(plain_text_password)
    return hashed_password


class UserRegistrationSchema(Schema):
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
