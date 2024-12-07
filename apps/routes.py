from flask import render_template, request, redirect, url_for, session
from .services import Services

def define_routes(app):
    """Define all application routes."""
    try:
        services = Services()

        # Home Page - Need to fill with best animation
        @app.route('/')
        def index():
            return "Welcome to the Sims App!"

        # Login Page - (Suppliers, Supervisor, Manager)
        @app.route('/login', methods=['GET', 'POST'])
        def login():
            return services.handle_login()

        # Supplier Home Page
        @app.route('/supplier/<int:user_id>/home', methods=['GET', 'POST'])
        def supplier_home(user_id):
            return services.supplier_home(user_id)
    
    except Exception as e:
        print(f"Exception in define routes : {str(e)}")