from flask import Flask
from flask import request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
import database_manager as dbHandler
import diary_management as diary
from flask import jsonify
import sqlite3 as sql

auth_key = "4L50v92nOgcDCYUM"

api = Flask(__name__)
cors = CORS(api)
api.config["CORS_HEADERS"] = "Content-Type"
limiter = Limiter(
    get_remote_address,
    app=api,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)


@api.route("/", methods=["GET"])
@limiter.limit("3/second", override_defaults=False)
def get():
    content = diary.diary_get()
    return (content), 200

@api.route("/add_diary", methods=["POST"])
@limiter.limit("1/second", override_defaults=False)
def post():
    if request.headers.get("Authorisation") == auth_key:
        data = request.get_json()
        response = diary.diary_add(data)
        return response
    else:
        return {"error": "Unauthorised"}, 401

api_log = logging.getLogger(__name__)
logging.basicConfig(
    filename="api_security_log.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


if __name__ == "__main__":
    api.run(debug=True, host="0.0.0.0", port=3000)