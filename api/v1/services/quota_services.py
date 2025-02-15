"""Quota service."""
from api.v1.services.dovecot_services import DovecotService
from database import DatabaseService
from schemas.email import Quota
from config import DatabaseName


class QuotaService():
    """Quota class"""
    def __init__(self):
        self.db_quota = DatabaseService(name=DatabaseName.QUOTA.value)

    def get_quota(self, email: str) -> Quota:
        """Get quota of a user."""
        quota = self.db_quota.find_text(text=email, split=True)
        if not quota:
            return Quota(quota_percent=0.0, quota=0, quota_used=0)
        quotaused, quotapercent = DovecotService().get_quota_used(email)
        return Quota(quota_percent=quotapercent, quota=quota[0][1], quota_used=quotaused)

    def add_quota(self, email: str, quota: float) -> Quota:
        """Set quota for a user."""
        existing_quota = self.db_quota.find_text(text=email)
        if existing_quota:
            self.db_quota.replace(text=[email, quota])
        else:
            self.db_quota.add(text=[email, quota])
        return self.get_quota(email)

    def remove_quota(self, email_id: str):
        """Remove quota for a user."""
        user = self.db_quota.find_text(text=email_id)
        if user:
            self.db_quota.remove(user[0])
