import os
from flask import Flask
from .routes import define_routes

def create_app():

    app = Flask(__name__, template_folder='../templates')

    # set the secret key
    app.secret_key = os.getenv("SECRET_KEY", "abcdefg")

    # Register routes
    define_routes(app)

    return app