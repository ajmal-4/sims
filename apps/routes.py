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
        
        # Supplier Add Client
        @app.route('/supplier/<int:user_id>/add_client', methods=['POST'])
        def add_client(user_id):
            return services.add_client(user_id)
        
        # Supplier Add Route
        @app.route('/supplier/<int:user_id>/add_route', methods=['POST'])
        def add_route(user_id):
            return services.add_route(user_id)
        
        # Supplier Sales deals
        @app.route('/supplier/<int:user_id>/sales', methods=['GET','POST'])
        def sales(user_id):
            return services.handle_sales(user_id)
        
        # Supplier daily route
        @app.route('/supplier/<int:user_id>/daily_route', methods=['GET','POST'])
        def daily_route(user_id):
            return services.daily_route(user_id)
        
        # Supplier - select route in daily route section
        @app.route('/supplier/<int:user_id>/daily_route/select_route', methods=['GET','POST'])
        def select_route(user_id):
            return services.select_route(user_id)

    
    except Exception as e:
        print(f"Exception in define routes : {str(e)}")