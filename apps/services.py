from datetime import datetime
from .common_services import CommonServices
from flask import Flask, request, render_template, redirect, url_for, session, jsonify
from .constants import HTMLPAGES, ErrorMessages, SuccessMessages, Limits, TransactionType
from .db import db
from pymongo import MongoClient
from bson import ObjectId
import gridfs
from .constants import HTMLPAGES, ERRORMESSAGES, SuccessMessages, Limits

fs = gridfs.GridFS(db)

class Services:
    def __init__(self) -> None:
        self.common_service = CommonServices()

    def handle_login(self):
        """Handles the login logic of different users"""
        try:

            if request.method == 'POST':
                
                username = request.form.get('username')
                password = request.form.get('password')

                # For debugging purposes
                print(f"Username : {username}")
                print(f"Password : {password}")

                # Authenticate user
                user_type, user_id = self.common_service.authenticate_user(username, password)
                print(user_type)
                print(user_id)
                
                # Check the user type and redirect to that template
                if user_type and user_id:
                    # Store user type in session
                    session['user_type'] = user_type
                    session['user_name'] = username
                    session['user_id'] = user_id

                    # Redirect to the appropriate home page
                    return redirect(url_for(f"{user_type}_home", user_id=user_id))
                
                else:
                    # Render login page with an error message
                    return render_template(HTMLPAGES.LOGIN_PAGE, error="Invalid credentials. Please try again.")
                
            # GET request: Render the login form
            return render_template(HTMLPAGES.LOGIN_PAGE)   
        
        except Exception as e:
            print(f"Exception in handle_login : {str(e)}")
            return render_template(HTMLPAGES.LOGIN_PAGE)
    

    def supplier_home(self, user_id):
        """Renders the supplier home page with routes, clients, sales and products based on the user_id."""
        try:

            routes = self.common_service.get_supplier_routes(user_id)
            clients = self.common_service.get_supplier_clients(user_id)
            products = self.common_service.get_supplier_products(user_id)
            sales = self.common_service.get_supplier_sales(user_id)

            return render_template(HTMLPAGES.SUPPLIER_HOME_PAGE, 
                                   user_id=user_id, 
                                   user_name=session.get('user_name'),
                                   user_type=session.get('user_type'),
                                   clients=clients, 
                                   products=products, 
                                   routes=routes,
                                   sales = sales
                                )
        
        except Exception as e:
            print(f"Exception in supplier_home : {str(e)}")
            return render_template(
                HTMLPAGES.ERROR_PAGE,
                e
            )
    

    def add_client(self, user_id, data):
        """Add new client into the database"""
        try:

            if request.method == 'POST':

                client_name = str(data.get('client_name'))
                client_phone = str(data.get('client_phone'))
                client_place = str(data.get('client_place'))
                route_no = str(data.get('route_no'))

                # Generate unique client_id dynamically
                client_id = f"client_{self.common_service.generate_unique_id('clients')}"
                
                # initially status and debt will be None
                status = None
                debt = None

                # Prepare the client data
                client_data = {
                    "client_id": client_id,
                    "name": client_name,
                    "phone_no": client_phone,
                    "place": client_place,
                    "route_no": route_no,
                    "status": status,
                    "debt": debt,
                    "supplier": str(user_id)
                }

                # Add client to MongoDB
                success = self.common_service.add_client_to_db(client_data)

                # Redirect or return an error message based on success
                if success:
                    if '_id' in client_data:
                        del client_data['_id']
                        return jsonify(client_data), 200
                else:
                    return ErrorMessages.ADD_CLIENT, 500

        except Exception as e:
            print(f"Exception in add_client : {str(e)}")
            return ErrorMessages.ADD_CLIENT, 500
    
    
    def edit_client(self, client_data):
        """Edit the existing client in the database"""
        try:

            client_id = client_data.get('client_id')
            update_data = {
                'name': client_data.get('name'),
                'place': client_data.get('place'),
                'route_no': client_data.get('route_no')
            }

            success = self.common_service.edit_client_from_db(client_id, update_data)
            
            if success:
                return jsonify({"message": SuccessMessages.EDIT_CLIENT}), 200
            else:
                return jsonify({"message": ErrorMessages.EDIT_CLIENT}), 500
        
        except Exception as e:
            print(f"Exception in edit_client : {str(e)}")
            return jsonify({"message": ErrorMessages.EDIT_CLIENT}), 500
    
    
    def delete_client(self, client_id):
        """Delete the existing client in the database"""
        try:
            success = self.common_service.delete_client_from_db(client_id)
            if success:
                return jsonify({"message": SuccessMessages.DELETE_CLIENT}), 200
            else:
                return jsonify({"message": ErrorMessages.DELETE_CLIENT}), 500

        except Exception as e:
            print(f"Exception in delete_client : {str(e)}")
            return jsonify({"message": ErrorMessages.DELETE_CLIENT}), 500
    
    def add_regular_products(self, user_id, data):
        try:
            regular_id = f"regular_{self.common_service.generate_unique_id('regulars')}"

            regular_data = {
                "regular_id": regular_id,
                "client_id": data.get("client_id"),
                "products": data.get("products"),
                "supplier": str(user_id)
            }

            success = self.common_service.add_regulars_products_to_db(regular_data)
            if success:
                return jsonify({"message": SuccessMessages.UPDATE_REGULAR_PRODUCTS}), 200
            else:
                return jsonify({"message": ErrorMessages.UPDATE_REGULAR_PRODUCTS}), 500

        except Exception as e:
            print(f"Exception in add_regular_products : {str(e)}")
            return jsonify({"message": ErrorMessages.UPDATE_REGULAR_PRODUCTS}), 500
    
    def fetch_regular_products(self, user_id, data):
        """ Fetch the regular products of a client """
        try:

            query = {
                "supplier" : str(user_id),
                "client_id" : data.get('client_id')
            }

            data = self.common_service.get_regular_products_from_db(query)
            if data:
                return jsonify({"success": True, "products": data.get("products",[])}), 200
            else:
                return jsonify({"success": False, "products": [], "message": ErrorMessages.FETCH_REGULAR_PRODUCTS}), 200

        except Exception as e:
            print(f"Exception in fetch_regular_products : {str(e)}")
            return jsonify({"success": False, "message": ErrorMessages.FETCH_REGULAR_PRODUCTS}), 404
    
    def add_client_payment(self, user_id, data):
        try:
            date = str(datetime.now())

            client_id = data.get("client_id", None)
            sale_id = data.get("sale_id", None)
            amount = data.get("amount", None)

            # Function to add to the sales data also while adding to the transaction.
            if client_id and sale_id and amount:
                # Add to the transaction first
                success = self.common_service.save_transaction_to_db(TransactionType.CREDIT, sale_id=sale_id, amount=amount, date=date, supplier=user_id, client=client_id)
                if success:
                    self.common_service.update_sales(sale_id, paid_amount=amount)
                    return jsonify({"success": True, "message": SuccessMessages.ADD_SALES_PAYMENT}), 200
                else:
                    return jsonify({"success": False, "message": ErrorMessages.ADD_SALES_PAYMENT}), 500
                
            elif client_id and amount:
                success = self.common_service.save_transaction_to_db(TransactionType.CREDIT, amount=amount, date=date, supplier=user_id, client=client_id)
                if success:
                    return jsonify({"success": True, "message": SuccessMessages.ADD_SALES_PAYMENT}), 200
                else:
                    return jsonify({"success": False, "message": ErrorMessages.ADD_SALES_PAYMENT}), 500

        except Exception as e:
            print(f"Exception in add_client_payment : {str(e)}")
    
    def fetch_client_payments(self, user_id, data):
        try:

            query = {"client":data.get("client"),"supplier":user_id}
            data = self.common_service.fetch_client_payment_history(query)
            if data:
                return jsonify({"success": True, "payments": data}), 200
            else:
                return jsonify({"success": False, "payments": [], "message": ErrorMessages.FETCH_RECENT_MONEY_TRANSACTIONS}), 200
            
        except Exception as e:
            print(f"Exception in fetch_client_payments : {str(e)}")
    
    def add_route(self, user_id):
        try:
            if request.method == 'POST':
                supplier = str(user_id)
                route_no = request.form.get('route_no')

                route_data = {
                    "supplier":supplier,
                    "route_no":route_no,
                    "clients":[]
                }

                # Add client to MongoDB
                success = self.common_service.add_route_to_db(route_data)

                # Redirect or return an error message based on success
                if success:
                    return redirect(url_for('supplier_home', user_id=user_id))
                else:
                    return "Error adding client", 500

        except Exception as e:
            print(f"Exception in add_route : {str(e)}")

    def add_product(self, user_id):
        """Add new products to the database"""
        try:
            if request.method == 'POST':

                product_id = f"product_{self.common_service.generate_unique_id('products')}"
                product_name = request.form.get('product_name')
                product_price = request.form.get('product_price')

                product_data = {
                    "product_id":product_id,
                    "product_name":product_name,
                    "product_price":product_price
                }

                success = self.common_service.add_product_to_db(product_data)

                # Redirect or return an error message based on success
                if success:
                    return redirect(url_for('supplier_home', user_id=user_id))
                else:
                    return "Error adding product", 500
                
        except Exception as e:
            print(f"Exception in add_product : {str(e)}")
    
    def handle_sales(self, user_id):
        """Redirect to the sales page"""
        try:
            return render_template(HTMLPAGES.SALES_PAGE, user_id=user_id)
        except Exception as e:
            print(f"Exception in add_product : {str(e)}")
            return render_template(HTMLPAGES.ERROR_PAGE)
    
    def handle_product_search(self, query):
        """Returns the product for the invoice creation"""
        try:
            products_list = self.common_service.get_similar_products(query)
            return products_list
        
        except Exception as e:
            print(f"Exception in handle_product_search : {str(e)}")
            return None
    
    def handle_product_price(self, product_name):
        """Returns the product price for the invoice creation"""
        try:
            product_price = self.common_service.get_product_price(product_name)
            return product_price
        
        except Exception as e:
            print(f"Exception in get_product_price : {str(e)}")
            return None
        
    def get_supplier_recent_sales(self, user_id, data):
        try:
            limit = data.get("limit", Limits.RECENT_SALE_DATA_LIMIT) 
            recent_sales = self.common_service.get_supplier_sales(user_id, limit=limit)

            if recent_sales:
                return jsonify({"success": True, "sale_data": recent_sales}), 200
            else:
                return jsonify({"success": False, "sale_data": [], "message": ErrorMessages.FETCH_RECENT_SALES_DATA}), 200

        except Exception as e:
            print(f"Exception in get_supplier_recent_sales : {str(e)}")
            return None
    
    def save_sales(self, data):
        """ Save the sales data into the database """
        try:
            sale_id = f"sale_{self.common_service.generate_unique_id('sales')}"

            sales_data = {
                "sale_id": sale_id,
                "client":data.get("client",''),
                "supplier": data.get("supplier", ''),
                "products": data.get("products", []),
                "total_amount": data.get("total_amount", 0.0),
                "date": data.get("date", datetime.now().isoformat()),
                "paid_amount": data.get("paid_amount", 0.0) # To be added.
            }

            result = self.common_service.save_sales_to_db(sales_data)
            if result:
                self.common_service.save_transaction_to_db(TransactionType.SALE, sale_id=sale_id)
                return jsonify({"success": True, "message": SuccessMessages.ADD_INVOICE}), 201
            else:
                return jsonify({"success": False, "message": ErrorMessages.ADD_INVOICE}), 500

        except Exception as e:
            print(f"Exception in save_invoice : {str(e)}")
            return None
    
    # To be added
    # def update_sales()
    
    def get_last_sales(self, user_id, data):
        """ Returns the last sales data of a client """
        try:
            query = {
                "supplier" : str(user_id),
                "client" : data.get('client')
            }

            if str(data.get('limit')) == str(Limits.LAST_SALE_DATA_LIMIT):
                data = self.common_service.get_supplier_last_sale_data(query)
                if data:
                    return jsonify({"success": True, "sale_data": data}), 200
                else:
                    return jsonify({"success": False, "sale_data": [], "message": ErrorMessages.FETCH_LAST_SALES_DATA}), 200
            
            else:
                data = self.common_service.get_supplier_recent_sales_data(query, Limits.RECENT_SALE_DATA_LIMIT)
                if data:
                    return jsonify({"success": True, "sale_data": data}), 200
                else:
                    return jsonify({"success": False, "sale_data": [], "message": ErrorMessages.FETCH_RECENT_SALES_DATA}), 200

        except Exception as e:
            print(f"Exception in get_last_sales : {str(e)}")
            return None
    
    def daily_route(self, user_id):
        try:
            # Retrieve all the routes
            routes = self.common_service.get_supplier_routes(user_id)
            clients = self.common_service.get_supplier_clients(user_id)
            products = self.common_service.get_supplier_products(user_id)
            sales = self.common_service.get_supplier_sales(user_id)
            # The current date
            selected_date = datetime.now().strftime("%Y-%m-%d")
            selected_routes = []

            if request.method == 'POST':
                # Retrieve selected date and route
                selected_date = request.form.get('date', selected_date)
                selected_routes = request.form.getlist('routes')

                print("selected routes : ",selected_routes)
                
                # Fetch clients for the selected route
                if selected_routes:
                    filtered_clients = self.common_service.get_clients_by_routes(user_id, selected_routes)
                else:
                    filtered_clients = clients

            return render_template(
                "supplier_home.html",
                user_id=user_id,
                user_name=session.get('user_name'),
                routes=routes,
                clients=clients,
                sales=sales,
                products=products,
                selected_date=selected_date,
                selected_routes=selected_routes,
                filtered_clients=filtered_clients
            )

        except Exception as e:
            print(f"Exception in daily_route : {str(e)}")
    
    def select_route(self, user_id):
        try:
            return self.daily_route(user_id)
        except Exception as e:
            print(f"Exception in select_route : {str(e)}")
    
    def fetch_daily_clients(self, user_id, data):
        try:

            selected_routes = data.get('routes')

            if selected_routes:
                filtered_clients = self.common_service.get_clients_by_routes(user_id, selected_routes)
            # need to update else condition
            else:
                filtered_clients = None

            if filtered_clients:
                return jsonify({"success": True, "clients": filtered_clients}), 200
            else:
                return jsonify({"success": False, "message": ErrorMessages.FETCH_CLIENTS}), 404
        except Exception as e:
            print(f"Exception in fetch_daily_clients : {str(e)}")
            return False
        
    def upload_image(self, image, user_id):
        """
        Upload profile image
        """
        try:
            # Store the image in GridFS
            image_id = fs.put(image, filename=image.filename, content_type=image.content_type)
            
            # Save user_id → image_id mapping in a collection
            self.common_service.save_image_to_db(image_id, user_id)

            return jsonify({"message": "Image uploaded successfully", "image_id": str(image_id)})
        except Exception as e:
            print(f"Exception in upload_image : {str(e)}")
            return False
    
    def get_image(self, user_id):
        """
        Get the image from GridFS
        """
        try:
            image_id = self.common_service.get_image_from_db(user_id)
            file = fs.get(image_id)
            return file.read(), 200, {"Content-Type": file.content_type}
        except Exception as e:
            return jsonify({"error": "Image not found"}), 404
    
