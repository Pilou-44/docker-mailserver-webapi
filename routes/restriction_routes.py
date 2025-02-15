"""Restriction"""
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from api.v1.services.restriction_services import RestrictionService
from api.v1.utils import RestrictionAccess
from config import DatabaseName
from database import DatabaseService
from schemas.restriction import Restriction

restriction_router = APIRouter(prefix='/restrict', tags=['Restriction'])


@restriction_router.get("/{email_id}")
async def get_restiction(email_id: str) -> Restriction:
    """Get restriction for a user.

    Args:
        email_id (str): The user.

    Raises:
        HTTPException: User doesn't exist.

    Returns:
        Restriction: The restriction object.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    user = db_account.find_text(text=email_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {email_id} does not exist")

    res_service = RestrictionService()
    return res_service.get_restriction(email=email_id)


@restriction_router.patch("")
async def update_restriction(email_id: str, access: RestrictionAccess) -> Restriction:
    """Update the restriction for a user.

    Args:
        email_id (str): The user.
        access (RestrictionAccess): The new restriction.

    Raises:
        HTTPException: User doesn't exist.

    Returns:
        Restriction: The new restriction.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    user = db_account.find_text(text=email_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {email_id} does not exist")

    res_service = RestrictionService()
    return res_service.update_restriction(email=email_id, acces=access)


@restriction_router.delete("/{email_id}", status_code=204)
async def delete_restriction(email_id: str, access: RestrictionAccess):
    """Delete the restriction for a user.

    Args:
        email_id (str): The user.
        access (RestrictionAccess): The new restriction (to remove)

    Raises:
        HTTPException: The updated restriction.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    user = db_account.find_text(text=email_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {email_id} does not exist")
    res_service = RestrictionService()
    res_service.update_restriction(email=email_id, acces=access)
