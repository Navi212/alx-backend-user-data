#!/usr/bin/env python3
"""
The `encrypt_password` module supplies `hash_password`
function that implements password salting and hashing
and `is_valid` function that compares a hashed_password
and string password if they compare equal/valid.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    hash_password:  A function that salts and hashes
                    a password and returns the hash

    Args:
    password:       A string that represents the password

    Return:
    hash:           A hashed byte string
    """
    passwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(passwd_bytes, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    is_valid:   A function that takes a hashed_password and
                string password as arguments and compares
                if they compare equal

    Args:
    hashed_password: A hashed_password in bytes
    password:        A string password

    Return:
    bool:       True/False if they compare equal/valid
    """
    password_bytes = password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_password)
