"""Models"""
from pydantic import BaseModel


class Restriction(BaseModel):
    """Restriction"""
    send: bool
    receive: bool
