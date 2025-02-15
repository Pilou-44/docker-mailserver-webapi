"""Models"""
from pydantic import BaseModel


class Alias(BaseModel):
    """Alias"""
    email_alias: str
    email_recipient: list[str]
