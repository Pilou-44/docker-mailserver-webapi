"""Models"""
from pydantic import BaseModel


class Alias(BaseModel):
    """Alias"""
    email_alias: str
    email_recipient: str


class Quota(BaseModel):
    """Quota"""
    quota: float
    quota_used: float
    quota_percent: float


class Restriction(BaseModel):
    """Restriction"""
    send: bool
    receive: bool


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
