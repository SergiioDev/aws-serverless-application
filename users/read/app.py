import bson
import ujson
from bson import ObjectId

from utils import db


def retrieve_info(object_id):
    mongo = db.MongoDBConnection()
    users = list()
    with mongo:
        database = mongo.connection["myDB"]
        collection = database["users"]

        if object_id is None:
            for data in collection.find():
                users.append({
                    "id": str(data["_id"]),
                    "email": str(data["email"]),
                    "username": str(data["username"]),
                    "first_name": str(data["first_name"]),
                })

            return users

        user = collection.find_one({"_id": ObjectId(object_id)})
        return {
            "email": str(user["email"]),
            "username": str(user["username"]),
            "first_name": str(user["first_name"]),
        }


def lambda_handler(event, context):
    try:
        object_id = event["pathParameters"]["id"]
    except Exception:
        object_id = None

    try:
        return {
            "statusCode": 200,
            "body": ujson.dumps({
                "message": "Success",
                "data": retrieve_info(object_id)
            })
        }

    except Exception as err:
        return {
            "statusCode": 400,
            "body": ujson.dumps({
                "message": "Something went wrong. Unable to parse data !",
                "error": str(err)
            })
        }
