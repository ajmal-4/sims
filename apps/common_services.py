class CommonServices:
    def authenticate_user(self, username, password):
        """Check if the provided username and password are correct."""
        try:
            # Replace with real authentication logic, e.g., database lookup
            valid_users = {
                "manager_1": {"password":"password123","type":"manager","id":"123"},
                "supervisor_1": {"password":"password123","type":"supervisor","id":"123"},
                "supplier_1": {"password":"password123","type":"supplier","id":"123"}
            }

            user = valid_users.get(username)
            if user and user.get('password') == password:
                return user.get('type'),user.get('id')
            return None
        
        except Exception as e:
            return None
    