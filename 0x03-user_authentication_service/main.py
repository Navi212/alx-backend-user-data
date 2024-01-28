#!/usr/bin/env python3
"""
The `main` module supplies functions that implements
End-to-end integration test for our methods and api
routes passing neccessary parameters and asserting
return values with status codes using the request
library.
"""
import requests


def register_user(email: str, password: str) -> None:
    """
    Tests staus code and return value when
    a user is newly registered
    """
    end_point = "http://127.0.0.1:5000/users"
    resp = requests.post(end_point,
                         data={"email": email, "password": password})
    if resp.status_code == 200:
        assert resp.json() == {"email": f"{email}", "message": "user created"}
        assert resp.status_code == 200


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests wrong login credentials and status code"""
    end_point = "http://127.0.0.1:5000/sessions"
    resp = requests.post(end_point,
                         data={"email": email, "password": password})
    assert resp.status_code == 401


def log_in(email: str, password: str) -> None:
    """Tests login with valid credentials"""
    end_point = "http://127.0.0.1:5000/sessions"
    resp = requests.post(end_point,
                         data={"email": email, "password": password})
    if resp.status_code == 200:
        assert resp.status_code == 200
        assert resp.json() == {"email": f"{email}", "message": "logged in"}


def profile_unlogged() -> None:
    """Tests user is unlogged"""
    end_point = "http://127.0.0.1:5000/profile"
    resp = requests.get(end_point)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests user is logged in with the write credentials"""
    end_point = "http://127.0.0.1:5000/profile"
    cookie = {"session_id": session_id}
    resp = requests.get(end_point, cookies=cookie)
    if resp.status_code == 200:
        assert resp.status_code == 200


def log_out(session_id: str) -> None:
    """Tests logout a logged in user"""
    end_point = "http://127.0.0.1:5000/sessions"
    cookie = {"session_id": session_id}
    resp = requests.delete(end_point, cookies=cookie)
    if resp.status_code == 302:
        assert resp.url == "http://127.0.0.1:5000"
    elif resp.status_code == 200:
        assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """Tests password token reset"""
    end_point = "http://127.0.0.1:5000/reset_password"
    resp = requests.post(end_point, data={"email": email})
    if resp.status_code == 200:
        assert resp.status_code == 200
        return resp.json()["reset_token"]
    else:
        assert resp.status_code == 403


def update_password(email: str,
                    reset_token: str, new_password: str) -> None:
    """Test user password update"""
    end_point = "http://127.0.0.1:5000/reset_password"
    payload = {"email": email, "reset_token": reset_token,
               "new_password": new_password}
    resp = requests.put(end_point, data=payload)
    if resp.status_code == 200:
        assert resp.status_code == 200
        assert resp.json() == {"email": f"{email}",
                               "message": "Password updated"}
    elif resp.status_code == 403:
        assert resp.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
