#!/usr/bin/env python3
"""Route module for the API"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
#auth = None
# Gets the auth type from enviroment variable `AUTH_TYPE`
#auth_type = os.getenv("AUTH_TYPE")

# If auth type is None, create new auth object
#if auth_type == "auth":
#    from api.v1.auth.auth import Auth
#    auth = Auth()
#elif auth_type == "basic_auth":
#    from api.v1.auth.basic_auth import BasicAuth
#    auth = BasicAuth()


#@app.before_request
#def before_request():
#    """Runs before any other function"""
 #   if auth is None:
 #       pass
 #   excluded_list = ['/api/v1/status/',
 #                    '/api/v1/unauthorized/', '/api/v1/forbidden/']
 #   if auth.require_auth(request.path, excluded_list):
 #       if auth.authorization_header(request) is None:
 #           abort(401, "error: Unauthorized")
 #       if auth.current_user(request) is None:
 #           abort(403, "error: Forbidden")


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def not_found(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
