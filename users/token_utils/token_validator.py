from argon2 import PasswordHasher
from marshmallow import Schema, fields, post_load, ValidationError

from utils import db
from token_utils import token


class RefreshTokenSchema(Schema):
    token = fields.Str(required=True)

    @post_load
    def validate_token(self, data, **kwargs):
        refresh_token = token.refresh_token(data['token'])
        if refresh_token['status']:
            data['token'] = refresh_token['data']
        else:
            raise ValidationError(refresh_token['message'])

        return data
