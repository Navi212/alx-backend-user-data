#!/usr/bin/env python3
"""The `session_exp_auth` module"""
from .session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """A class that sets expiration time on sessions"""
    def __init__(self):
        try:
            time_duration = int(os.getenv("SESSION_DURATION"))
        except Exception:
            time_duration = 0
        self.session_duration = time_duration

    def create_session(self, user_id=None):
        """
        Creates a session through the parent class create_session
        method using super() to call parent method
        """
        session_id = super().create_session(user_id)
        if session_id is None or not session_id:
            return None
        session_dictionary = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overload. Returns user id for the current session"""
        if session_id is None:
            return None
        details = self.user_id_by_session_id.get(session_id)
        if session_id is None:
            return None
        elif self.session_duration <= 0:
            return details.get("user_id")
        elif "created_at" not in details.keys():
            return None
        created_at = details.get("created_at")
        allowed_time = created_at + timedelta(seconds=self.session_duration)
        if allowed_time < datetime.now():
            return None
        return details.get("user_id")
