from .db import db

class CommonServices:

    def __init__(self):
        self.clients = db.get_collection('clients')
        self.routes = db.get_collection('routes')
        self.products = db.get_collection('products')

    # For authenticating the user - returns the user_type if the user is valid else returns None
    def authenticate_user(self, username, password):
        """Check if the provided username and password are correct."""
        try:
            # Replace with real authentication logic, e.g., database lookup
            valid_users = {
                "manager_1": {"password":"password123","type":"manager","id":"123"},
                "supervisor_1": {"password":"password123","type":"supervisor","id":"123"},
                "supplier_1": {"password":"password123","type":"supplier","id":"123"},
                "supplier_2": {"password":"password123","type":"supplier","id":"321"}
            }

            user = valid_users.get(username)
            if user and user.get('password') == password:
                return user.get('type'), user.get('id')
            return None, None
        
        except Exception as e:
            print(f"Exception in authenticate_user : {str(e)}")
            return None, None
    
    
    # ----------------------------------- #
    #               Retrievals            #
    # ----------------------------------- #
    
    def get_all_routes(self):
        """ Each route will have unique route_no and clients """
        try:
            
            # Uncomment if not connected to mongo db 
            # routes = [
            #     {"route_no":"1","supplier":"123","clients":["client_1","client_2"]},
            #     {"route_no":"2","supplier":"321","clients":["client_3","client_4"]}
            # ]

            routes = list(self.routes.find())
            print("routes",routes)

            return routes

        except Exception as e:
            print(f"Exception in all_routes : {str(e)}")
            return None
    
    def get_supplier_routes(self, supplier_id):
        """ Get the list of all clients of the supplier in that route """
        try:

            # all_routes = self.get_all_routes()
            # supplier_routes = [
            #     route for route in all_routes if route.get('supplier') == str(supplier_id)
            # ] 
            self.get_all_routes()
            supplier_routes = list(self.routes.find({"supplier": str(supplier_id)}))
            print("supplier_routes : ",supplier_routes)
            return supplier_routes
        
        except Exception as e:
            print(f"Exception in get_supplier_routes : {str(e)}")
            return None

    
    # Dummy clients - Need to replace with actual clients from database
    def all_clients(self):
        try:
            """ Each client will have unique client_id, name, place, route_no and the supplier """

            # clients = [
            #     {"client_id":"client_1","name":"ajmal","place":"wky","route_no":"1","status":"cleared","debt":None,"supplier":"123"},
            #     {"client_id":"client_2","name":"mishal","place":"pavaratty","route_no":"2","status":"debt","debt":"100","supplier":"321"}
            # ]

            clients = list(self.clients.find())
            return clients
        
        except Exception as e:
            print(f"Exception in all_clients : {str(e)}")
            return None
    
    # Get the list of all clients of the supplier
    def get_supplier_clients(self, supplier_id):
        try:

            # Get all clients
            # clients = self.all_clients()
            # Get the clients of the parfticular supplier
            # supplier_clients = [
            #     client for client in clients if client.get("supplier") == str(supplier_id)
            # ]

            supplier_clients = list(self.clients.find({"supplier": str(supplier_id)}))
            return supplier_clients
        
        except Exception as e:
            print(f"Exception in get_supplier_clients : {str(e)}")
            return None
    
    def get_all_products(self):
        try:

            # products = [
            #     {"product_id":"product_1","product_name":"milk","product_price":"28"},
            #     {"product_id":"product_2","product_name":"biscuit","product_price":"40"}
            # ]

            products = list(self.products.find())
            return products
        
        except Exception as e:
            print(f"Exception in get_all_products : {str(e)}")
            return None
    
    def get_supplier_products(self, supplier_id):
        try:
            
            all_products = self.get_all_products()
            return all_products

        except Exception as e:
            print(f"Exception in get_supplier_products : {str(e)}")
            return None
    
    def get_clients_by_routes(self, user_id, selected_routes):
        try:
            return list(self.clients.find({"supplier": str(user_id), "route_no": {"$in": selected_routes}}))
        except Exception as e:
            pass
    

    # ----------------------------------- #
    #               Adding                #
    # ----------------------------------- #

    def add_client_to_db(self, client_data):
        """ Adds new client to the database """
        try:
            self.clients.insert_one(client_data)
            return True
        except Exception as e:
            print(f"Exception in add_client_to_db : {str(e)}")
            return False
    
    def add_route_to_db(self, route_data):
        """ Adds new supplier route to the database """
        try:
            self.routes.insert_one(route_data)
            return True
        except Exception as e:
            print(f"Exception in add_client_to_db : {str(e)}")
            return False