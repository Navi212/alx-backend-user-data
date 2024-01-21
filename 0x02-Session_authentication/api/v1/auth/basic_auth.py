#!/usr/bin/env python3
"""The `basic_auth` module supplies a class BasicAuth"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """BasicAuth sub classes Auth class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts authorization header"""
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        try:
            header = authorization_header.split()
            if header[0] != "Basic":
                return None
            return header[1]
        except IndexError:
            pass

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Returns the decoded value of a Base64string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None
        try:
            if not base64.b64decode(base64_authorization_header):
                return None
            return base64.b64decode(
                base64_authorization_header).decode("utf-8")
        except Exception:
            pass

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        elif ":" not in decoded_base64_authorization_header:
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")
        if len(credentials) > 2:
            email = credentials[0]
            password = ":".join(credentials[1:])
            if email and password:
                return (email, password)
        email, password = decoded_base64_authorization_header.split(":")
        if email and password:
            return (email, password)
        return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Retrieves user object from useremail and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        elif user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search({"email": user_email})
        if user_list is None or not user_list:
            return None
        for user in user_list:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns current user"""
        header = self.authorization_header(request)
        if header:
            base64_header = self.extract_base64_authorization_header(header)
            if base64_header:
                decoded = self.decode_base64_authorization_header(
                    base64_header)
                if decoded:
                    email, password = self.extract_user_credentials(
                        decoded)
                    if email:
                        return self.user_object_from_credentials(
                            email, password)
