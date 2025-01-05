from flask import jsonify
from .db import db

class CommonServices:

    def __init__(self):
        self.clients = db.get_collection('clients')
        self.routes = db.get_collection('routes')
        self.products = db.get_collection('products')
        self.sales = db.get_collection('sales')
        self.users = db.get_collection('users')

    # For authenticating the user - returns the user_type if the user is valid else returns None
    def authenticate_user(self, username, password):
        """Check if the provided username and password are correct."""
        """Returns the 'type' and 'id' if login is successfull, else None, None"""
        try:
            
            user = self.users.find_one({"username": username})
        
            if user and user.get("password") == password:
                return user.get("type"), user.get("id")

            # Return None, None if authentication fails
            return None, None
        
        except Exception as e:
            print(f"Exception in authenticate_user : {str(e)}")
            return None, None
    

    #--------------------------------------#
    #        Generating Unique ID          #
    #--------------------------------------#

    def generate_unique_id(self, collection_name):
        """Generate unique id for products, clients, users, routes, sales"""
        try:
            counter = db.get_collection("counters").find_one_and_update(
                {"_id": collection_name},
                {"$inc": {"value": 1}},
                upsert=True,
                return_document=True
            )

            return counter.get('value','abc')
        
        except Exception as e:
            print(f"Exception in generate_unique_id : {str(e)}")
            return 'abc'
    
    
    # ----------------------------------- #
    #               Retrievals            #
    # ----------------------------------- #


    # # # Routes # # #
    
    def get_all_routes(self):
        """ Retrieves all routes from the database """
        """ Each route will have unique route_no and clients """
        try:
            
            # Uncomment if not connected to mongo db 
            # routes = [
            #     {"route_no":"1","supplier":"123","clients":["client_1","client_2"]},
            #     {"route_no":"2","supplier":"321","clients":["client_3","client_4"]}
            # ]

            routes = list(self.routes.find())
            print("routes", routes)

            return routes

        except Exception as e:
            print(f"Exception in all_routes : {str(e)}")
            return None
    
    def get_supplier_routes(self, supplier_id):
        """ Get the list of all clients of the supplier in that route """
        try:
 
            supplier_routes = list(self.routes.find({"supplier": str(supplier_id)}))
            print("supplier_routes : ",supplier_routes)

            return supplier_routes
        
        except Exception as e:
            print(f"Exception in get_supplier_routes : {str(e)}")
            return None

    
    # # # Clients # # #

    def all_clients(self):
        try:
            """ Retrieves all clients from the database """
            """ Each client will have unique client_id, name, place, route_no and the supplier """

            clients = list(self.clients.find())
            return clients
        
        except Exception as e:
            print(f"Exception in all_clients : {str(e)}")
            return None
    
    # Get the list of all clients of the supplier
    def get_supplier_clients(self, supplier_id):
        """ Get the list of all clients of the supplier """
        try:

            supplier_clients = list(self.clients.find({"supplier": str(supplier_id)}))
            return supplier_clients
        
        except Exception as e:
            print(f"Exception in get_supplier_clients : {str(e)}")
            return None
    
    def get_clients_by_routes(self, user_id, selected_routes):
        try:
            return list(self.clients.find({"supplier": str(user_id), "route_no": {"$in": selected_routes}}))
        except Exception as e:
            pass
        
    
    # # # Products # # #
    
    def get_all_products(self):
        """ Retrieves all products from the database """
        try:

            products = list(self.products.find())
            return products
        
        except Exception as e:
            print(f"Exception in get_all_products : {str(e)}")
            return None
    
    def get_supplier_products(self, supplier_id):
        """ Retrieves all products of the supplier from the database """
        try:
            
            all_products = self.get_all_products()
            return all_products

        except Exception as e:
            print(f"Exception in get_supplier_products : {str(e)}")
            return None
    
    def get_similar_products(self, query):
        """Retrieves the similar products to a product query"""
        try:
            products = self.products.find({"product_name": {"$regex": query, "$options": "i"}})
            product_list = [{"product_name": product['product_name'], "product_price": product['product_price']} for product in products]
            return jsonify(product_list)
        
        except Exception as e:
            print(f"Exception in get_supplier_products : {str(e)}")
            return None
    
    def get_product_price(self, product_name):
        """Returns the price of the product"""
        try:
            product = self.products.find_one({"product_name": product_name})
            if product:
                return jsonify({"product_price": product['product_price']})
            return jsonify({"product_price": 0})
        
        except Exception as e:
            print(f"Exception in get_supplier_products : {str(e)}")
            return None
    
    
    # # # Sales # # #

    def get_all_sales_list(self):
        """Returns all the sales data"""
        try:
            
            all_sales_list = list(self.sales.find())
            return all_sales_list
        
        except Exception as e:
            print(f"Exception in get_sales_list : {str(e)}")
            return None
    
    def get_supplier_sales(self, supplier_id):
        """Returns all the sales data of the supplier"""
        try:

            supplier_sales_list = list(self.sales.find({"supplier": str(supplier_id)}))
            return supplier_sales_list

        except Exception as e:
            print(f"Exception in get_supplier_sales : {str(e)}")
            return None
    

    # ----------------------------------- #
    #               Adding                #
    # ----------------------------------- #

    def add_users_to_db(self, users):
        try:
            # Flatten the structure for each user
            flattened_users = []
            for user in users:
                for username, details in user.items():
                    flattened_users.append({
                        "username": username,
                        **details
                    })

            # Insert the flattened data into the collection
            # result = collection.insert_many(flattened_users)
            self.users.insert_many(flattened_users)
            return True
        except Exception as e:
            print(f"Exception in add_user_to_db : {str(e)}")
            return False

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
    
    def add_product_to_db(self, product_data):
        try:
            self.products.insert_one(product_data)
            return True
        except Exception as e:
            print(f"Exception in add_product_to_db : {str(e)}")
            return False
    

    def save_invoice_to_db(self, invoice):
        try:
            result = self.sales.insert_one(invoice)
            return jsonify({"message": "Invoice saved successfully!", "invoice_id": str(result.inserted_id)}), 201
        except Exception as e:
            print(f"Exception in save_invoice_to_db : {str(e)}")
            return False


