from api.v1.services.dovecot_services import DovecotService
from database import DatabaseService
from schemas.email import Quota
from config import DatabaseName


class QuotaService():
    """as"""
    def __init__(self):
        self.db_virtual = DatabaseService(name=DatabaseName.QUOTA.value)

    def get_quota(self, email: str) -> Quota:
        """ga"""
        quota = self.db_virtual.find_text(text=email, split=True)
        if not quota:
            return Quota(quota_percent=0.0, quota=0, quota_used=0)
        quotaused, quotapercent = DovecotService().get_quota_used(email)
        return Quota(quota_percent=quotapercent, quota=quota[0][1], quota_used=quotaused)
