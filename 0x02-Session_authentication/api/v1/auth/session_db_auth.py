#!/usr/bin/env python3
"""The `session_db_auth` module supplies a SessionDBAuth class"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """A subclass of `SessionExpAuth`"""
    def create_session(self, user_id=None):
        """
        Creates and stores new instance of UserSession
        and returns the Session ID
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
            "user_id": user_id,
            "session_id": session_id
        }
        user = UserSession(**session_dict)
        user.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user id by requesting the db based on session_id"""
        user_id = UserSession.search({"session_id": session_id})
        if not user_id:
            return None
        return user_id

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID from
        the request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False
        user_session[0].remove()
        return True
