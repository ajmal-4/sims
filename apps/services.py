from flask import Flask, request, render_template, redirect, url_for, session
from common_services import CommonServices

class Services:
    def __init__(self) -> None:
        self.common_service = CommonServices

    def handle_login(self):
        """Handles the login logic."""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            # Authenticate user
            user_type, user_id = self.common_service.authenticate_user(username, password)
            # Check the user type and redirect to that template
            if user_type:
                # Store user type in session
                session['user_type'] = user_type
                session['user_name'] = username
                session['user_id'] = user_id

                # Redirect to the appropriate home page
                return redirect(url_for(f"{user_type}_home"))
            else:
                # Render login page with an error message
                return render_template('login.html', error="Invalid credentials. Please try again.")

        # GET request: Render the login form
        return render_template('login.html')
    
    def supplier_home(self, user_id):
        """Renders the supplier home page with clients and products."""
        clients = self.common_service.get_all_clients(user_id)
        products = self.common_service.get_all_products(user_id)

        return render_template('supplier_home.html', user_id=user_id, user_name=session.get('user_name'), clients=clients, products=products)
