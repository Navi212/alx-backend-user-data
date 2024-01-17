#!/usr/bin/env python3
"""
The `basic_auth` module supplies a class `BasicAuth`
that inherits from the base `Auth` class
"""
import base64
from models.user import User
from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    """Defines a subclass `BasicAuth` of `Auth` class"""
    pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization header"""
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        elif not authorization_header.split()[0] == "Basic":
            return None
        return authorization_header.split()[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        Returns the decoded value of a Base64 string
        base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_str = base64.b64decode(base64_authorization_header
                                           ).decode("utf-8")
            if decoded_str:
                return decoded_str
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """Returns the user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        elif not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        credentials = decoded_base64_authorization_header.split(":")
        if len(credentials) > 2:
            email = credentials[0]
            password = ":".join(credentials[1:])
            if email and password:
                return (email, password)
        elif ":" in decoded_base64_authorization_header:
            email, password = decoded_base64_authorization_header.split(":")
            if email and password:
                return (email, password)
        return (None, None)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        user_list = User.search({"email": user_email})
        if user_list is None or not user_list:
            return None
        for user in user_list:
            if user.is_valid_password(user_pwd):
                return user
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        if auth_header:
            base64_header = self.extract_base64_authorization_header(
                auth_header)
            if base64_header:
                decoded_header = self.decode_base64_authorization_header(
                    base64_header)
                if decoded_header:
                    email, password = self.extract_user_credentials(
                        decoded_header)
                    if email:
                        return self.user_object_from_credentials(
                            email, password)
        return
