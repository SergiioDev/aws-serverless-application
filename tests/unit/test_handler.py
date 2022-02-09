import json
import pytest
from users.create import app
from users.utils import db


@pytest.fixture()
def fixture_event():
    return {
        "body": "{\"email\": \"sergi88@gmail.com\", \"username\": \"sergiomaster\", \"first_name\": \"sergi\", \"password\": \"sergi123\"}"
    }


class TestRegistrationAPI:
    def test_labmda_handler(self, fixture_event):
        registration = app.lambda_handler(fixture_event, "")
        data = json.loads(registration["body"])

        assert registration["statusCode"] == 201
        assert "message" in registration["body"]
        assert data["message"] == "Registered Successfully"

    def teardown(self):
        mongo = db.MongoDBConnection()
        with mongo:
            database = mongo.connection['myDB']
            collection = database['users']

            users = collection.find().sort([("_id", -1)])
            for user in users:
                user_id = user["_id"]

            collection.delete_one({"_id": user_id})

