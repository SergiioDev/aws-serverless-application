import bson
import ujson
from bson import ObjectId
from utils import db, validator


def lambda_handler(event, context):
    try:
        object_id = event["pathParameters"]["id"]
    except Exception:
        object_id = None

    mongo = db.MongoDBConnection()
    with mongo:
        database = mongo.connection['myDB']
        collection = database['users']
        try:
            collection.delete_one({"_id": ObjectId(object_id)})
        except bson.errors.InvalidId:
            return {
                "statusCode": 400,
                "body": ujson.dumps({
                    "message": "Error deleting the user, invalid ID"
                })
            }

        return {
            "statusCode": 200,
            "body": ujson.dumps({
                "message": "Data deleted Successfully!"
            })
        }
