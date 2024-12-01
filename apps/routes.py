from flask import request, jsonify


def define_routes(app):
    """Define all application routes."""

    @app.route('/')
    def home():
        return "Welcome to the Sims App!"