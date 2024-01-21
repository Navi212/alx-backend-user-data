#!/usr/bin/env python3
"""
The `user_session` module supplies a class that implements
a session db (file) storage
"""
from .base import Base


class UserSession(Base):
    """Inherits from Base"""
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
