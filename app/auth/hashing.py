"""
This module provides functions for hashing and verifying passwords using the pwdlib library.

It includes a dummy hash for timing attack prevention when verifying passwords.
"""
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def verify_password_dummy(password: str) -> bool:
    """
    Verify password against a dummy hash to mitigate timing attacks.
    
    This function should be called when a user is not found during authentication to ensure consistent response times.
    
    Always returns False.
    """
    password_hash.verify(password, DUMMY_HASH)
    return False
