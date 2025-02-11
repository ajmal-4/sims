from flask import jsonify
from .db import db
from pymongo import DESCENDING
from .constants import SuccessMessages, ErrorMessages, Projections, PaymentStatus, TransactionType, Limits

class CommonServices:

    def __init__(self):
        self.clients = db.get_collection('clients')
        self.routes = db.get_collection('routes')
        self.products = db.get_collection('products')
        self.sales = db.get_collection('sales')
        self.transactions = db.get_collection('transactions')
        self.users = db.get_collection('users')
        self.regulars = db.get_collection('regulars')
        self.user_images = db.get_collection('user_images')

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

            routes = list(self.routes.find())
            return routes

        except Exception as e:
            print(f"Exception in all_routes : {str(e)}")
            return None
    
    def get_supplier_routes(self, supplier_id):
        """ Get the list of all clients of the supplier in that route """
        try:
 
            supplier_routes = list(self.routes.find({"supplier": str(supplier_id)}))
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

            supplier_clients = list(self.clients.find({"supplier": str(supplier_id)}, {"_id": 0}))
            return supplier_clients
        
        except Exception as e:
            print(f"Exception in get_supplier_clients : {str(e)}")
            return None
    
    def get_clients_by_routes(self, user_id, selected_routes):
        try:
            
            return list(self.clients.find(
                {"supplier": str(user_id), "route_no": {"$in": selected_routes}},
                Projections.EXCLUDE_ID
            ))
    
        except Exception as e:
            print(f"Exception in get_supplier_clients : {str(e)}")
            return None
        
    
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
            if products:
                product_list = [{"product_name": product['product_name'], "product_price": product['product_price']} for product in products]
                return jsonify(product_list)
            else:
                return None
        
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
    
    def get_supplier_sales(self, supplier_id, **kwargs):
        """ Returns all the sales data of the supplier """
        try:
            query = {"supplier": str(supplier_id)}

            if kwargs.get("limit"):
                limit = kwargs.get("limit")
                supplier_sales_list = list(self.sales.find(query, Projections.EXCLUDE_ID).sort("date", DESCENDING).limit(limit))
            else:
                supplier_sales_list = list(self.sales.find(query, Projections.EXCLUDE_ID))

            return supplier_sales_list

        except Exception as e:
            print(f"Exception in get_supplier_sales : {str(e)}")
            return None
    
    def get_supplier_last_sale_data(self, query):
        """ Returns the last sale data of the supplier """
        try:
            result = self.sales.find_one(query, Projections.EXCLUDE_ID, sort=[("date", -1)])
            return result
        
        except Exception as e:
            print(f"Exception in get_supplier_last_sale_data : {str(e)}")
            return None
    
    def get_supplier_recent_sales_data(self, query, limit):
        try:
            result = list(self.sales.find(query, Projections.EXCLUDE_ID).sort("date", DESCENDING).limit(limit))
            return result
        
        except Exception as e:
            print(f"Exception in get_supplier_recent_sales_data : {str(e)}")
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
            result = self.clients.insert_one(client_data)
            if result.inserted_id:
                return True
            else:
                return False
            
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
    

    def save_sales_to_db(self, sales_data):
        try:
            result = self.sales.insert_one(sales_data)
            return bool(result.inserted_id)
            
        except Exception as e:
            print(f"Exception in save_invoice_to_db : {str(e)}")
            return False
    
    def update_sales(self, sale_id, **kwargs):
        try:
            if kwargs.get("paid_amount"):
                update_data = {"paid_amount": kwargs.get("paid_amount")}
            else:
                pass
            
            result = self.sales.update_one(
                        {'sale_id': sale_id}, 
                        {'$set': update_data}
                    )
            if result.modified_count > 0:
                return True
            else:
                return False
            
        except Exception as e:
            print(f"Exception in update_sales : {str(e)}")
            return False
    
    
    def  save_transaction_to_db(
        self, 
        transaction_type : TransactionType,
        **kwargs
    ):
        """ save the transactions to db """
        """ transactions can be either a sale or a cash credit """
        """ for sale, inputs are transaction_type : 'sale' and transaction_type_id : 'sale_id' """
        """ for cash credit transaction_type : 'credit' , transaction_type_id : 'credit_id' and receives 'amount' and 'date' as kwargs"""
        try:
            
            transaction_id = self.generate_unique_id('transaction')

            transaction_data = {
                "transaction_id" : transaction_id,
                "transaction_type" : transaction_type.value
            }

            sale_id = kwargs.get("sale_id", None)
            if sale_id:
                transaction_data["sale_id"] = sale_id

            amount = kwargs.get("amount", None)
            date = kwargs.get("date", None)
            client_id = kwargs.get("client", None)
            supplier_id = kwargs.get("supplier", None)

            if transaction_type == TransactionType.CREDIT and amount and date:
                transaction_data["amount"] = amount
                transaction_data["date"] = date
                transaction_data["client"] = client_id
                transaction_data["supplier"] = supplier_id
            
            result = self.transactions.insert_one(transaction_data)
            
            return bool(result)         

        except Exception as e:
            print(f"Exception in save_transaction_to_db : {str(e)}")
            return False
    
    def edit_client_from_db(self, client_id, update_data):
        try:
            result = self.clients.update_one(
                        {'client_id': client_id}, 
                        {'$set': update_data}
                    )
            
            if result.modified_count > 0:
                return True
            else:
                return False
            
        except Exception as e:
            print(f"Exception in edit_client_from_db : {str(e)}")
            return False
    
    def delete_client_from_db(self, client_id):
        try:
            result = self.clients.delete_one({"client_id": str(client_id)})
            if result.deleted_count > 0:
                return True
            else:
                return False
        except Exception as e:
            print(f"Exception in edit_client_from_db : {str(e)}")
            return False
        
    def save_image_to_db(self, image_id, user_id):
        try:
            result = self.user_images.update_one(
                {"user_id": user_id}, {"$set": {"image_id": image_id}}, upsert=True)
            if result.image_id:
                return True
            else:
                return False
        except Exception as e:
            print(f"Exception in save_image_to_db : {str(e)}")
            return False
        
    def get_image_from_db(self, user_id):

        try:
            image_id = self.user_images.find_one({'user_id': user_id}).get('image_id')
            return image_id
        except Exception as e:
            print(f"Exception in get_image_from_db : {str(e)}")
            return False

    def add_regulars_products_to_db(self, regular_data):
        try:
            
            result = self.regulars.update_one(
                {"client_id": str(regular_data.get("client_id"))},
                {"$set": regular_data},
                upsert=True
            )

            if result.matched_count > 0 or result.upserted_id is not None:
                return True
            else:
                return False

        except Exception as e:
            print(f"Exception in edit_client_from_db : {str(e)}")
            return False
    
    def get_regular_products_from_db(self, query):
        try:
            result = self.regulars.find_one(query, Projections.EXCLUDE_ID)
            if result:
                return result
            else:
                return False

        except Exception as e:
            print(f"Exception in get_regular_products_from_db : {str(e)}")
            return False
    
    def fetch_client_payment_history(self, query):
        try:
            result = list(self.transactions.find(query, Projections.EXCLUDE_ID).sort("date", DESCENDING).limit(Limits.RECENT_SALE_DATA_LIMIT))
            return result
        
        except Exception as e:
            return None