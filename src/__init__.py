from flask import Flask, jsonify
import os
from src.auth import auth
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.posts import posts
from src.database import db
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from
from src.config.swapper import template, swagger_config

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        
        app.config.from_mapping(
            SECRET_KEY =os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            SQL_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),

            SWAGGER = {
                "title" : "Blog Posts API",
                "uiversion" : 3
            }
        )
    
    else:

        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)

    JWTManager(app)

    app.register_blueprint(auth)
    app.register_blueprint(posts)

    Swagger(app, config=swagger_config, template=template)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error":"Not Found"}), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"error":"Something went wrong!!!"}), HTTP_500_INTERNAL_SERVER_ERROR
    
    return app
