#!/usr/bin/env python3
"""
The `session_auth` module creates a new Flask view
that handles all routes for the Session authentication.
"""
from api.v1.views import app_views
from flask import request, jsonify
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def login():
    """Implements an authentication, and login session"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email == "" or not email:
        return jsonify({"error": "email missing"}), 400
    if password == "" or not password:
        return jsonify({"error": "password missing"}), 400
    user_list = User.search({"email": email})
    if not user_list or user_list is None:
        return jsonify({"error": "no user found for email"}), 404
    for user in user_list:
        from api.v1.app import auth
        from os import getenv
        session_id = auth.create_session(user.id)
        user_id = auth.user_id_for_session_id(session_id)
        response = jsonify(user_id.to_json())
        session_name = getenv("SESSION_NAME")
        response.set_cookie(session_name, session_id)
        return response
    return jsonify({"error": "wrong password"}), 401
