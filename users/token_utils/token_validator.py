from argon2 import PasswordHasher
from marshmallow import Schema, fields, post_load, ValidationError

from utils import db
from token_utils import token


class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def validate_email_password(self, data, **kwargs):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['myDB']
            collection = database['users']
            user = collection.find_one({"email": data['email']})
            is_password_correct = PasswordHasher().verify(user['password'], data['password'])

            if user is not None and is_password_correct:
                data['token'] = token.create_access_token(user)

            if user is None or not is_password_correct:
                raise ValidationError("Email or password invalid")

            return data


class RefreshTokenSchema(Schema):
    token = fields.Str(required=True)

    @post_load
    def validate_token(self, data, **kwargs):
        refresh_token = token.refresh_access_token(data['token'])
        if refresh_token['status'] == "success":
            data['token'] = refresh_token['data']
        if refresh_token['status'] == "failed":
            raise ValidationError(refresh_token['message'])

        return data
