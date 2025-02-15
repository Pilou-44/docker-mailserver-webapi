"""Custom exception and utilities"""
from enum import Enum


class EmailNotFoundException(Exception):
    """Email not found exception."""


class EmailExistException(Exception):
    """Email already exist exception"""


class RestrictionAccess(Enum):
    """Restriction"""
    SEND = "send"
    RECV = "receive"
