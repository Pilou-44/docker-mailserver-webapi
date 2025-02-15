"""Models"""
from pydantic import BaseModel


class Quota(BaseModel):
    """Quota"""
    quota: float
    quota_used: float
    quota_percent: float


class QuotaCreate(BaseModel):
    """QuotaCreate"""
    email: str
    newquota: float
