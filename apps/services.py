from flask import Flask, request, render_template, redirect, url_for, session
from datetime import datetime
from .common_services import CommonServices

class Services:
    def __init__(self) -> None:
        self.common_service = CommonServices()

    def handle_login(self):
        try:
            """Handles the login logic."""
            if request.method == 'POST':
                
                username = request.form.get('username')
                password = request.form.get('password')

                # For debugging purposes
                print(f"Username : {username}")
                print(f"Password : {password}")

                # Authenticate user
                user_type, user_id = self.common_service.authenticate_user(username, password)
                # Check the user type and redirect to that template
                if user_type:
                    # Store user type in session
                    session['user_type'] = user_type
                    session['user_name'] = username
                    session['user_id'] = user_id

                    # Redirect to the appropriate home page
                    return redirect(url_for(f"{user_type}_home",user_id=user_id))
                else:
                    # Render login page with an error message
                    return render_template('login.html', error="Invalid credentials. Please try again.")
            # GET request: Render the login form
            return render_template('login.html')   
        except Exception as e:
            print(f"Exception in handle_login : {str(e)}")
    
    def supplier_home(self, user_id):
        try:
            """Renders the supplier home page with routes, clients and products."""
            routes = self.common_service.get_supplier_routes(user_id)
            clients = self.common_service.get_supplier_clients(user_id)
            products = self.common_service.get_supplier_products(user_id)

            return render_template('supplier_home.html', 
                                   user_id=user_id, 
                                   user_name=session.get('user_name'), 
                                   clients=clients, 
                                   products=products, 
                                   routes=routes
                                )
        except Exception as e:
            print(f"Exception in supplier_home : {str(e)}")
    
    def add_client(self, user_id):
        try:
            if request.method == 'POST':
                # Retrieve client details from the form
                client_name = request.form.get('client_name')
                client_place = request.form.get('client_place')
                route_no = request.form.get('route_no')
                status = request.form.get('status') or None
                debt = request.form.get('debt') or None

                # client_id = f"client_{self.common_service.generate_unique_id('clients')}"  # Generate unique client ID
                # Need to change this to generate an automatic unique_id
                client_id = request.form.get('client_id')

                # Prepare the client data
                client_data = {
                    "client_id": client_id,
                    "name": client_name,
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
                    # return "Hooraayy!! success!!"
                    return redirect(url_for('supplier_home', user_id=user_id))
                else:
                    return "Error adding client", 500

        except Exception as e:
            print(f"Exception in add_client : {str(e)}")
    
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
                    # return "Hooraayy!! success!!"
                    return redirect(url_for('supplier_home', user_id=user_id))
                else:
                    return "Error adding client", 500

        except Exception as e:
            pass
    
    def handle_sales(self, user_id):
        try:
            pass
        except Exception as e:
            pass
    
    def daily_route(self, user_id):
        try:
            # Retrieve all the routes
            routes = self.common_service.get_supplier_routes(user_id)
            clients = self.common_service.get_supplier_clients(user_id)
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
                routes=routes,
                clients=clients,
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
