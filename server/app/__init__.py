"""
shorter - A small API for URL shortening.
"""

import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, g
from flask_pymongo import PyMongo
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


@app.route("/")
def home():
    return {"message": "Welcome to the default (root) handler."}


@app.route("/v1/url/<shortcode>", methods=["GET"])
def get(shortcode):
    # Using the shortcode, return the full url to the client
    return shortcode


@app.route("/v1/url", methods=["POST"])
def create_shortcode():
    # Using the full url, create the DB entry and return the shortcode to the client
    return request.data
