from flask import render_template, request, redirect, url_for, session
from .services import Services

def define_routes(app):
    """Define all application routes."""
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
    @app.route('/supplier/<int:supplier_id>/home', methods=['GET', 'POST'])
    def supplier_home(supplier_id):
        return services.supplier_home()