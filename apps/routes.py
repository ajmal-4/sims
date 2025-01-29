from flask import render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from pydantic import ValidationError

from .services import Services
from .constants import ErrorMessages
from .common_services import CommonServices
from .schemas import RegularProductsRequest

def define_routes(app):
    """Define all application routes."""
    try:
        services = Services()
        common_service = CommonServices()

        # Home Page - Need to fill with best animation
        @app.route('/')
        def index():
            return "Welcome to the Sims App!"

        # Login Page - (Suppliers, Supervisors, Managers)
        @app.route('/login', methods=['GET', 'POST'])
        def login():
            return services.handle_login()


        # ---------------------------------- #
        #        Supplier Home Page          #
        # ---------------------------------- #
        
        # supplier main page 
        @app.route('/supplier/<int:user_id>/home', methods=['GET', 'POST'])
        def supplier_home(user_id):
            return services.supplier_home(user_id)
        
        
        ### Client ###

        # Supplier Add Client
        @app.route('/supplier/<int:user_id>/add_client', methods=['POST'])
        def add_client(user_id):
            data = request.get_json()
            return services.add_client(user_id, data)
        
        # Supplier Edit Client
        @app.route('/supplier/<int:user_id>/edit_client', methods=['POST'])
        def edit_client(user_id):
            data = request.get_json()
            return services.edit_client(data)
        
        # Supplier Delete Client
        @app.route('/supplier/<int:user_id>/delete_client', methods=['POST'])
        def delete_client(user_id):
            data = request.get_json()
            client_id = data.get('client_id')
            return services.delete_client(client_id)
        

        ### Regular ###

        #supplier Add Client's regular
        @app.route('/supplier/<int:user_id>/add_regular', methods = ['GET','POST'])
        def add_regular(user_id):
            try:
                # Validate and parse request JSON
                data = RegularProductsRequest.model_validate(request.get_json())
                return services.add_regular_products(user_id, data.model_dump())
        
            except ValidationError as e:
                print(f"Exception in add_regular : {str(e)}")
                return jsonify({"message": ErrorMessages.UPDATE_REGULAR_PRODUCTS}), 500
        
        ### Route ###

        # Supplier Add Route
        @app.route('/supplier/<int:user_id>/add_route', methods=['POST'])
        def add_route(user_id):
            return services.add_route(user_id)
        
        ### Product ###
        
        # Supplier Add Product
        @app.route('/supplier/<int:user_id>/add_product', methods=['POST'])
        def add_product(user_id):
            return services.add_product(user_id)
        
        ### sales ###

        # Redirect to Supplier sales page
        @app.route('/supplier/<int:user_id>/sales', methods=['GET','POST'])
        def sales(user_id):
            return services.handle_sales(user_id)
        
        # Get list of all clients 
        @app.route('/get_clients/<int:user_id>', methods=['GET'])
        def get_clients(user_id):
            clients = common_service.get_supplier_clients(user_id)
            return jsonify({"clients": clients})
        
        # Similar Product Search for sales form
        @app.route('/get_similar_products', methods=['GET'])
        def get_similar_products():
            query = request.args.get('query', '')
            return services.handle_product_search(query)
        
        # Fetch Product Price
        @app.route('/get_product_price', methods=['GET'])
        def get_product_price():
            product_name = request.args.get('product_name', '')
            return services.handle_product_price(product_name)
        
        # Save the sales data
        @app.route('/save_sales/<int:user_id>', methods=['POST'])
        def save_sales(user_id):
            data = request.get_json()
            if not data:
                return jsonify({"error": "No data provided"}), 400
            else:
                return services.save_sales(data)
        
        # Get the last sales data of a client
        @app.route('/get_last_sale/<int:user_id>', methods=['GET'])
        def get_last_sale(user_id):
            data = {
                'client' : request.args.get('client','other'),
                'limit' : request.args.get('limit', 1)
            }
            if data:
                return services.get_last_sales(user_id, data)
        
        @app.route('/update_sales/<int:user_id>', methods=['PUT'])
        def update_sales(user_id):
            print("hj")

        ### Daily Route ###
        
        # Supplier daily route
        @app.route('/supplier/<int:user_id>/daily_route', methods=['GET','POST'])
        def daily_route(user_id):
            return services.daily_route(user_id)
        
        # Supplier - select route in daily route section
        @app.route('/supplier/<int:user_id>/daily_route/select_route', methods=['GET','POST'])
        def select_route(user_id):
            return services.select_route(user_id)
        
        @app.route('/fetch_daily_clients/<int:user_id>', methods=['GET','POST'])
        def fetch_daily_clients(user_id):
            data = request.get_json()
            return services.fetch_daily_clients(user_id, data)

    
    except Exception as e:
        print(f"Exception in define routes : {str(e)}")