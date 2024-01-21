#!/usr/bin/env python3
"""
The `session_auth` module creates a new Flask view
that handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from models.user import User
from flask import request, jsonify, abort
import os


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login_session():
    """Implements an authentication, and login session"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email == "" or not email:
        return jsonify({"error": "email missing"}), 400
    elif password == "" or not password:
        return jsonify({"error": "password missing"}), 400
#   Search the user list in the database and return the
#   list for a particular email address if found
    user_list = User.search({"email": email})
    if not user_list or user_list is None:
        return jsonify({"error": "no user found for this email"})
    for user in user_list:
        # Vet the user password passed via the request with the
        # with the password in the user list if they compare same
        if user.is_valid_password(password):
            from api.v1.app import auth
            # Create a session id for the valid user
            session_id = auth.create_session(user.id)
            json_response = jsonify(user.to_json())
            session_name = os.getenv("SESSION_NAME")
            json_response.set_cookie(session_name, session_id)
            return json_response
        return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def logout_session():
    """Deletes a user from a session on logout"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
