import datetime
import os
import jwt


def create_access_token(result):
    jwt_info = jwt.encode({
        "id": str(result["_id"]),
        "first_name": result["first_name"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=300)}, os.environ['SECRET_KEY'],"HS256")

    return jwt_info


def refresh_token(token):
    try:
        print(token)
        result = jwt.decode(token, str(os.environ['SECRET_KEY']), "HS256")
        jwt_info = jwt.encode({**result, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=300)},
                              os.environ['SECRET_KEY'])

        return {"status": True, "data": jwt_info, "message": None}
    except jwt.ExpiredSignatureError:
        return {"status": False, "data": None, "message": "Token has expired !"}
    except jwt.exceptions.DecodeError:
        return {"status": False, "data": None, "message": "Unable to decode data !"}

