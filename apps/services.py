from flask import request, render_template, redirect, url_for

def authenticate_user(username, password):
    """Check if the provided username and password are correct."""
    # Replace with real authentication logic, e.g., database lookup
    valid_users = {
        "admin": "password123",
        "user": "mypassword"
    }
    return valid_users.get(username) == password

def handle_login():
    """Handles the login logic."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Authenticate user
        if authenticate_user(username, password):
            return redirect(url_for('home'))
        else:
            return "Invalid credentials. Please try again.", 401

    return render_template('login.html')
