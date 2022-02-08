import bson
import ujson
from bson import ObjectId
from utils import db, validator


def lambda_handler(event, context):
    try:
        object_id = event["pathParameters"]["id"]
    except Exception:
        object_id = None

    body = ujson.loads(event["body"])
    result = validator.UserUpdateSchema()

    if result.validate(body) is not None:
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['myDB']
            collection = database['users']
            try:
                collection.update_one({"_id": ObjectId(object_id)}, {"$set": body})
            except bson.errors.InvalidId:
                return {
                    "statusCode": 400,
                    "body": ujson.dumps({
                        "message": "Error updating the user, invalid ID"
                    })
                }

            return {
                "statusCode": 200,
                "body": ujson.dumps({
                    "message": "Data Updated Successfully!",
                    "data": result.dump(body)
                })
            }
