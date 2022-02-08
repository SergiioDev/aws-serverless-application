import datetime
import os
import jwt


def create_access_token(result):
    access_token = jwt.encode({
        "id": result["_id"],
        "email": result["email"],
        "username": result["username"],
        "first_name": result["first_name"],
        "expiration": datetime.datetime.utcnow() + datetime.timedelta(seconds=300)}, os.environ['SECRET_KEY'])

    return access_token


def refresh_access_token(token):
    try:
        result = jwt.decode(token, os.environ['SECRET_KEY'])
        jwt_info = jwt.encode({**result, "expiration": datetime.datetime.utcnow() + datetime.timedelta(seconds=300)},
                              os.environ['SECRET_KEY'])
        return {"status": "success", "data": jwt_info.decode()}
    except jwt.exceptions.DecodeError:
        return {"status": "failed", "message": "Unable to decode data"}
    except jwt.ExpiredSignatureError:
        return {"status": "failed", "message": "Token has expired"}
