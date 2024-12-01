from flask import Flask
from .routes import define_routes

def create_app():

    app = Flask(__name__, template_folder='../templates')

    # Register routes
    define_routes(app)

    return app