from flask import render_template, request, redirect, url_for
from .services import handle_login

def define_routes(app):
    """Define all application routes."""

    # Home Page - Need to fill with best animation
    @app.route('/')
    def home():
        return "Welcome to the Sims App!"
    
    # Login Page - (Suppliers, Supervisor, Manager)
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return handle_login()