#!/usr/bin/env python3
"""
The `session_auth` module creates a new Flask view
that handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def session_login():
    """Implements an authentication, and login session"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email == "" or email is None:
        return jsonify({"error": "email missing"}), 400
    if password == "" or password is None:
        return jsonify({"error": "password missing"}), 400
    user_list = User.search({"email": email})
    if not user_list or user_list is None:
        return jsonify({"error": "no user found for this email"}), 404
    for user in user_list:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_cookie = auth.create_session(user.id)
            response = jsonify(user.to_json())
            session_name = os.getenv("SESSION_NAME")
            response.set_cookie(session_name, session_cookie)
            return response
        return jsonify({"error": "wrong password"}), 401


@app_views.route('/api/v1/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def session_logout():
    """Deletes a user from a session on logout"""
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
