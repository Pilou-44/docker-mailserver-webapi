"""Models"""
from pydantic import BaseModel


class Fail2banJail(BaseModel):
    """Fail2banJail"""
    name: str
    currently_banned: int
    total_banned: int
    banned_ips: list[str]
