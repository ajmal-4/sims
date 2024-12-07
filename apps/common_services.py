class CommonServices:
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
    
    # Dummy clients - Need to replace with actual clients from database
    def all_clients(self):
        try:
            """ Each client will have unique client_id, name, place, route_no and the supplier """

            clients = [
                {"client_id":"client_1","name":"ajmal","place":"wky","route_no":"1","status":"cleared","debt":None,"supplier":"123"},
                {"client_id":"client_2","name":"mishal","place":"pavaratty","route_no":"2","status":"debt","debt":"100","supplier":"321"}
            ]

            return clients
        except Exception as e:
            print(f"Exception in all_clients : {str(e)}")
            return None
    
    def get_supplier_routes(self, supplier_id):
        try:
            pass
        except Exception as e:
            pass
    
    # Get the list of all clients of the supplier
    def get_supplier_clients(self, supplier_id):
        try:
            # Get all clients
            clients = self.all_clients()

            # Get the clients of the parfticular supplier
            supplier_clients = [
                client for client in clients if client.get("supplier") == str(supplier_id)
            ]

            return supplier_clients
        
        except Exception as e:
            print(f"Exception in get_supplier_clients : {str(e)}")
            return None
    
    def get_supplier_products(self, user_id):
        try:
            pass
        except Exception as e:
            pass

    