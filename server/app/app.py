"""
shorter - A small API for URL shortening.
"""
import datetime
import os

from models.url import UrlModel
from schemas.url import CreateUrlInputSchema
from schemas.auth import AuthInputSchema
from dotenv import load_dotenv
from flask import Flask, request, g, Response, jsonify, make_response
from flask_pymongo import PyMongo
from nanoid import generate
from pymongo import IndexModel
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError

load_dotenv()


def get_db(instance: Flask):
    if 'db' not in g:
        g.db = PyMongo(instance)

    return g.db


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.getenv("SECRET_KEY"),
        MONGO_URI=os.getenv("MONGO_URI")
    )

    return app


app = create_app()
with app.app_context():
    mongo = get_db(app)

urls: Collection = mongo.db.urls

shortcode_index = IndexModel("shortcode", unique=True)
created_at_index = IndexModel("created_at")
urls.create_indexes([shortcode_index, created_at_index])

alphabet = '23456789bcdfghjkmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'


@app.route("/")
def home():
    return {"message": "Welcome to the default (root) handler."}


@app.route("/v1/url/<shortcode>", methods=["GET"])
def get(shortcode):
    query = {"shortcode": shortcode}
    result_count = urls.count_documents(query)
    if result_count == 0:
        return make_response(jsonify({
            "status": "SHORTCODE_NOT_FOUND"
        }), 404)

    result = urls.find_one(query, {'_id': 0, 'full_url': 1})

    resp = {
        "status": "success",
        "full_url": result['full_url']
    }

    return make_response(jsonify(resp))


@app.route("/v1/url", methods=["POST"])
def create_shortcode():
    schema = CreateUrlInputSchema()
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return make_response(jsonify({
            "status": "failure :sad_face:"
        }), 400)

    full_url = data['full_url']
    # TODO: If we receive a shortcode, ensure it only contains allowed characters
    shortcode = data['shortcode'] if 'shortcode' in data.keys() else generate(alphabet, size=8)

    # if full_url is already present, return the existing shortcode and extend expires_at by a month
    query = {"full_url": full_url}
    count = urls.count_documents(query)

    if count != 0:
        existing = urls.find_one(query, {'_id': 0, 'shortcode': 1, 'expires_at': 1})
        urls.update_one(query, {'$set': {'expires_at': existing['expires_at'] + datetime.timedelta(weeks=4)}})
        resp = {
            "status": "success",
            "shortcode": existing['shortcode'],
            "expires_at": existing['expires_at']
        }

        return make_response(jsonify(resp))

    model = UrlModel(full_url, shortcode, request.remote_addr)

    try:
        urls.insert_one(model.json())
    except DuplicateKeyError:
        resp = make_response("{'status': 'failure', 'message': 'SHORTCODE_ALREADY_EXISTS'}", 400)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    created_response_json = {
        "status": "success",
        "shortcode": model.shortcode,
        "expires_at": model.expires_at
    }

    return make_response(jsonify(created_response_json))


@app.route("/v1/url/purge-expired", methods=["POST"])
def purge_expired():
    query = {"expires_at": {"$lte": datetime.datetime.now()}}
    results = urls.delete_many(query)
    return make_response(jsonify({
        "status": "success",
        "deleted": results.deleted_count
    }))

@app.route("/v1/auth", methods=["POST"])
def auth():
    schema = AuthInputSchema()
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return make_response(jsonify({
            "status": "failure :sad_face:"
        }), 400)

    password = data['password']
    if password == os.getenv("APP_AUTH_PASSWORD"):
        return make_response(jsonify({
           "auth": "success"
        }), 200)

    return make_response(jsonify({
       "auth": "failure"
    }), 401)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    return response
