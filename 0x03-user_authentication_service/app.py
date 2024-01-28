#!/usr/bin/env python3
"""
The `app` module supplies our Flask app routes for different
api end_points.
"""
from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound
from db import DB


AUTH = Auth()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    """Returns a json payload for the root route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users() -> str:
    """Register user"""
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        _ = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login() -> str:
    """Logins in a user to a session and sets a session id to cookie"""
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password) is False:
        abort(401)
    session_id = AUTH.create_session(email)
    resp = jsonify({"email": f"{email}", "message": "logged in"})
    resp.set_cookie("session_id", session_id)
    return resp


@app.route("/sessions", methods=["DELETE"])
def logout() -> str:
    """Logs out a user from a session and redirects to root '/' route"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile() -> str:
    """Serves get request for user profile"""
    session_id = request.cookies.get("session_id", None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"}), 200
    abort(403)


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token() -> str:
    """Resets a password field"""
    email = request.form.get("email")
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": f"{email}", "reset_token": f"{token}"}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Updates password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify(
            {"email": f"{email}", "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
