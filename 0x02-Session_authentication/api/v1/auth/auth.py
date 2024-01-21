#!/usr/bin/env python3
"""The `auth` module"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """A class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Requires authentication method"""
        if path is None or excluded_paths is None or len(excluded_paths) < 1:
            return True
        if path in excluded_paths:
            return False
        if not path.endswith("/"):
            path = path + "/"
            if path in excluded_paths:
                return False
        # Implements wildcard functionality
        for paths in excluded_paths:
            wild_path = paths.split("/")
            last_path = wild_path[-1]
            if last_path.endswith("*"):
                l_path = last_path.split("*")[0]
                if l_path in path:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """Checks Authorization header for requests"""
        if request is None:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current user object of User class"""
        return None

    def session_cookie(self, request=None):
        """Returns the a cookie value/session_id as cookie value"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        value = request.cookies.get(session_name)
        return value
