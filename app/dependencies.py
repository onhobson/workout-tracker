"""
Centralized dependencies for the workout tracker application.
"""
from app.db.dependencies import DbSession
from app.auth.dependencies import CurrentUser

__all__ = ["DbSession", "CurrentUser"]