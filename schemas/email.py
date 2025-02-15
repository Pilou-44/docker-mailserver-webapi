"""Models"""
from pydantic import BaseModel

from schemas.alias import Alias
from schemas.quota import Quota
from schemas.restriction import Restriction


class Email(BaseModel):
    """User"""
    username: str
    password: str
    quota: Quota
    alias: list[Alias]
    restriction: Restriction


class EmailCreate(BaseModel):
    """EmailCreate"""
    email: str
    password: str
