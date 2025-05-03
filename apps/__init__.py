import os
from flask import Flask
from .routes import define_routes
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*")

def create_app():

    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    # set the secret key
    app.secret_key = os.getenv("SECRET_KEY", "abcdefg")

    # Register routes
    define_routes(app, socketio)

    socketio.init_app(app)
    
    return app, socketio