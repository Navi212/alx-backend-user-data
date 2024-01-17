#!/usr/bin/env python3
"""The `auth` module supplies a class `Auth`"""
from flask import request
from typing import List, TypeVar


class Auth:
    """A base class for Authentication"""
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
        """
        Checks Authorization header and returns the
        value for the Authorization header
        """
        if request is None:
            return None
        elif not request.headers.get("Authorization"):
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Checks current user"""
        return None
