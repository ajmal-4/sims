from flask import render_template, request, redirect, url_for, session, jsonify
from datetime import datetime
from pydantic import ValidationError
from flask_socketio import join_room, leave_room

from .services import Services
from .constants import ErrorMessages
from .common_services import CommonServices
from .schemas import (RegularProductsRequest, FetchClientRecentSales, FetchSupplierRecentSales, 
                      AddPayment, FetchPaymentHistory, FetchClientStatus, SupplyRegular, FetchRegularProducts,
                      FetchDailyClients, UpdateSales, AddDailyExpense, GetDailyExpense, UpdateLocation, GetLocation)

connected_users = {}

def define_routes(app, socketio):
    """Define all application routes."""
    try:
        services = Services()
        common_service = CommonServices()

        # Home Page - Need to fill with best animation
        @app.route('/')
        def index():
            return "Welcome to the Sims App!"
        
        # Websocket connection
        @socketio.on('connect')
        def on_connect():
            print(f"New client connected: {request.sid}")
        
        @socketio.on('join')
        def handle_join(data):
            user_id = data.get("user_id")
            role = data.get("role")
            sid = request.sid

            if user_id:
                connected_users[sid] = {
                    "user_id": user_id,
                    "role": role
                }

                join_room(user_id)

                print(f"{role} '{user_id}' joined. SID: {sid}")
                socketio.emit("user_connected", {"message": f"{user_id} connected"})
        
        @socketio.on('disconnect')
        def on_disconnect():
            sid = request.sid
            user = connected_users.pop(sid, None)
            if user:
                leave_room(user["user_id"])
                print(f"{user['role']} '{user['user_id']}' disconnected.")
            else:
                print(f"Unknown user disconnected. SID: {sid}")
        
        @socketio.on('assign_task')
        def assign_task(data):
            supplier_id = data.get("supplier_id")
            task = data.get("task")

            # Example: Save to DB (you can use your service here)
            # services.save_assignment(...)

            # Send task to that supplier
            socketio.emit("new_assignment", {"task": task}, room=supplier_id)
            print(f"Task sent to supplier: {supplier_id}")


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
        
        
        ### Client
        #################

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
        
        # Fetch client's recent sales
        @app.route('/supplier/<int:user_id>/get_client_recent_sales', methods=['POST'])
        def fetch_client_recent_sales(user_id):
            try:
                data = FetchClientRecentSales.model_validate(request.get_json())
                return services.get_last_sales(user_id, data.model_dump())

            except ValidationError as e:
                print(f"Exception in fetch_client_recent_sales : {str(e)}")
                return jsonify({"message": ErrorMessages.FETCH_RECENT_SALES_DATA}), 500
        
        # Fetch Supplier's recent sales
        @app.route('/supplier/<int:user_id>/get_recent_sales', methods=['POST'])
        def fetch_recent_sales(user_id):
            try:
                data = FetchSupplierRecentSales.model_validate(request.get_json())
                return services.get_supplier_recent_sales(user_id, data.model_dump())
            except ValidationError as e:
                print(f"Exception in fetch_client_recent_sales : {str(e)}")
                return jsonify({"message": ErrorMessages.FETCH_RECENT_SALES_DATA}), 500
        
        # Fetch client debt status
        @app.route('/supplier/<int:user_id>/get_client_status', methods=['POST'])
        def get_client_status(user_id):
            try:
                data = FetchClientStatus.model_validate(request.get_json())
                return services.get_client_status(user_id, data.model_dump())
            except ValidationError as e:
                print(f"Exception in fetch_client_recent_sales : {str(e)}")
                return jsonify({"message": ErrorMessages.FETCH_CLIENT_STATUS}), 500

        ### Regular Products
        ###########################

        #supplier Add Client's regular
        @app.route('/supplier/<int:user_id>/add_regular', methods = ['GET','POST'])
        def add_regular(user_id):
            try:
                # Validate and parse request JSON
                data = RegularProductsRequest.model_validate(request.get_json())
                return services.add_regular_products(user_id, data.model_dump())
        
            except ValidationError as e:
                print(f"Exception in /add_regular : {str(e)}")
                return jsonify({"message": ErrorMessages.UPDATE_REGULAR_PRODUCTS}), 500
        
        #supplier Fetch Client's Regular
        @app.route('/supplier/<int:user_id>/get_regular', methods = ['GET','POST'])
        def get_regular(user_id):
            try:
                data = FetchRegularProducts.model_validate(request.get_json())
                return services.fetch_regular_products(user_id, data.model_dump())
            
            except ValidationError as e:
                print(f"Exception in /get_regular : {str(e)}")
                return jsonify({"message": ErrorMessages.FETCH_REGULAR_PRODUCTS}), 500


        ### Route
        ################

        # Supplier Add Route
        @app.route('/supplier/<int:user_id>/add_route', methods=['POST'])
        def add_route(user_id):
            return services.add_route(user_id)
        
        ### Product
        ###################
        
        # Supplier Add Product
        @app.route('/supplier/<int:user_id>/add_product', methods=['POST'])
        def add_product(user_id):
            return services.add_product(user_id)
        
        ### sales
        ################

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
        
        # Get the last sales data of a client (load last sales)
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
            try:
                data = UpdateSales.model_validate(request.get_json())
                return services.update_sales(user_id, data.model_dump())

            except ValidationError as ve:
                print(f"Validation error in /update_sales : {str(ve)}")
                return jsonify({"message": ErrorMessages.UPDATE_INVOICE}), 500


        ### Payment Transactions
        ###############################

        # Add the payment
        @app.route('/supplier/<int:user_id>/payment', methods=['POST'])
        def payment(user_id):
            try:
                data = AddPayment.model_validate(request.get_json())
                return services.add_client_payment(user_id, data.model_dump())

            except ValidationError as e:
                print(f"Exception in payment : {str(e)}")
            
            except Exception as e:
                print(f"{str(e)}")
        
        # Fetch client's recent payment history
        @app.route('/supplier/<int:user_id>/get_payment_history', methods=['POST'])
        def fetch_money_transactions(user_id):
            try:
                data = FetchPaymentHistory.model_validate(request.get_json())
                return services.fetch_client_payments(user_id, data.model_dump())
            
            except ValidationError as e:
                print(f"Exception in fetch_money_transactions : {str(e)}")
                return jsonify({"message": ErrorMessages.FETCH_RECENT_MONEY_TRANSACTIONS}), 500


        ### Daily Route
        ######################
        
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
            try:
                data = FetchDailyClients.model_validate(request.get_json())
                return services.fetch_daily_clients(user_id, data.model_dump())
            except ValidationError as e:
                print(f"Exception in /fetch_daily_clients : {str(e)}")
                return jsonify({"message": ErrorMessages.FETCH_DAILY_ROUTE_CLIENTS}), 500

        @app.route('/supplier/<int:user_id>/supply_regular', methods=['GET', 'POST'])
        def supply_regular(user_id):
            try:
                data = SupplyRegular.model_validate(request.get_json())
                return services.supply_regular(user_id, data.model_dump())
            except ValidationError as e:
                print(f"Exception in /supply_regular : {str(e)}")
                return jsonify({"message": ErrorMessages.SUPPLY_REGULAR}), 500
    
        @app.route('/supplier/<int:user_id>/add_daily_expense', methods=['POST'])
        def add_daily_expense(user_id):
            try:
                data = AddDailyExpense.model_validate(request.get_json())
                return services.add_daily_expense(user_id, data.model_dump())
            
            except ValidationError as e:
                print(f"Exception in /add_daily_expense : {str(e)}")
                return jsonify({"message": ErrorMessages.ADD_DAILY_EXPENSE}), 500

        @app.route('/supplier/<int:user_id>/get_daily_expense', methods=['GET', 'POST'])
        def get_daily_expense(user_id):
            try:
                data = GetDailyExpense.model_validate(request.get_json())
                return services.get_daily_expense(user_id, data.model_dump())
            except ValidationError as e:
                print(f"Exception in /get_daily_expense : {str(e)}")
                return jsonify({"message": ErrorMessages.GET_DAILY_EXPENSE}), 500
        
        ### Location
        ##################

        @app.route('/supplier/<int:user_id>/update_location', methods=['GET', 'POST'])
        def update_location(user_id):
            try:
                data = UpdateLocation.model_validate(request.get_json())
                return services.update_location(user_id, data.model_dump())
            except ValidationError as e:
                print(f"Exception in /update_location : {str(e)}")
                return jsonify({"message": ErrorMessages.UPDATE_LOCATION}), 500
        
        @app.route('/supplier/<int:user_id>/get_location', methods=['GET', 'POST'])
        def get_location(user_id):
            try:
                data = GetLocation.model_validate(request.get_json())
                return services.fetch_location(user_id, data.model_dump())
            except ValidationError as e:
                print(f"Exception in /update_location : {str(e)}")
                return jsonify({"message": ErrorMessages.UPDATE_LOCATION}), 500       

    except Exception as e:
        print(f"Exception in define routes : {str(e)}")