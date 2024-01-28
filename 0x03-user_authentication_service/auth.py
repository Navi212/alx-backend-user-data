#!/usr/bin/env python3
"""The `auth` module supplies a method `_hash_password`"""
import bcrypt
from db import DB
from user import User
from typing import TypeVar, Union
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns the salted hash"""
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(bytes, salt)


def _generate_uuid() -> str:
    """Generates a uuid str and returns it"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar("User"):
        """Registers a user by email and password"""
        try:
            _ = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks email and password if its a valid login"""
        try:
            user = self._db.find_user_by(email=email)
            bytes = password.encode("utf-8")
            if bcrypt.checkpw(bytes, user.hashed_password):
                return True
            return False
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Creates a session for a user and returns the session id"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self,
                                 session_id: str
                                 ) -> Union[TypeVar("User"), None]:
        """Returns corresponding User or None from session_id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session by user id"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Resets an email password token with uuid"""
        try:
            user = self._db.find_user_by(email=email)
            reset_token_uuid = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token_uuid)
            return reset_token_uuid
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates password for existing email"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=hashed_pwd, reset_token=None)
        except NoResultFound:
            raise ValueError
