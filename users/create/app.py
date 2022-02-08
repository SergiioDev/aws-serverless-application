import json
import ujson
from marshmallow import ValidationError
from utils import db, validator


def lambda_handler(event, context):
    try:
        print(event)
        body = ujson.loads(event["body"])
        user = validator.UserRegistrationSchema()

        if user is not None:
            mongo = db.MongoDBConnection()
            with mongo:
                database = mongo.connection["myDB"]
                collection = database["users"]
                collection.insert_one(user.load(body))
            return {
                "statusCode": 201,
                "body": ujson.dumps({
                    "message": "Registered Successfully",
                    "data": user.validate(body)
                })
            }

    except ValidationError as err:
        return {
            "statusCode": 400,
            "body": ujson.dumps({
                "message": err.messages
            })
        }

    except KeyError:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Something went wrong, unable to parse data!"
            })
        }
