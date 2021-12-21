"""
shorter - A small API for URL shortening.
"""
import datetime
import os

from app.models.url import UrlModel
from app.schemas.url import CreateUrlInputSchema
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
    # Using the shortcode, return the full url to the client
    return shortcode


@app.route("/v1/url", methods=["POST"])
def create_shortcode():
    schema = CreateUrlInputSchema()
    data = request.get_json()
    errors = schema.validate(data)

    if errors:
        return Response("{'status': 'failure :sad_face:'}", status=400, mimetype='application/json')

    full_url = data['full_url']
    # TODO: If we receive a shortcode, ensure it only contains allowed characters
    shortcode = data['shortcode'] if 'shortcode' in data.keys() else generate(alphabet, size=8)

    # if full_url is already present, return the existing shortcode and extend expires_at by a month
    query = {"full_url": full_url}
    count = urls.count_documents(query)

    if count is not 0:
        existing = urls.find_one(query, {'_id': 0, 'shortcode': 1, 'expires_at': 1})
        urls.update_one(query, {'$set': {'expires_at': existing['expires_at'] + datetime.timedelta(weeks=4)}})
        resp = {
            "status": "success",
            "shortcode": existing['shortcode']
        }

        return jsonify(resp)

    model = UrlModel(full_url, shortcode, request.remote_addr)

    try:
        urls.insert_one(model.json())
    except DuplicateKeyError:
        resp = make_response("{'status': 'failure', 'message': 'SHORTCODE_ALREADY_EXISTS'}", 400)
        resp.headers['Content-Type'] = 'application/json'
        return resp

    created_response_json = {
        "status": "success",
        "shortcode": model.shortcode
    }

    return jsonify(created_response_json)
