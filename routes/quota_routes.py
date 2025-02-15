""""Quota"""
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from api.v1.services.quota_services import QuotaService
from config import DatabaseName
from database import DatabaseService
from schemas.email import Quota
from schemas.quota import QuotaCreate

quota_router = APIRouter(prefix='/quota', tags=['Quota'])


@quota_router.post("")
async def add_quota(quota: QuotaCreate) -> Quota:
    """Set quota for a user.

    Args:
        quota (QuotaCreate): The user and quota amount to set.

    Raises:
        HTTPException: User doesn't exist.

    Returns:
        Quota: The new quota.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    user = db_account.find_text(text=quota.email)
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {quota.email} does not exist")

    quota_service = QuotaService()
    new_quota = quota_service.add_quota(email=quota.email, quota=quota.newquota)
    return new_quota


@quota_router.delete("/{email_id}", status_code=204)
async def delete_quota(email_id: str):
    """Remove quota for a user.

    Args:
        email_id (str): The user to remove the quota for.

    Raises:
        HTTPException: User doesn't exist.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    user = db_account.find_text(text=email_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {email_id} does not exist")
    quota_service = QuotaService()
    quota_service.remove_quota(email_id=email_id)
