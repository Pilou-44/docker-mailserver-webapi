"""Alias"""
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from api.v1.services.alias_services import AliasService
from schemas.email import Alias
from config import DatabaseName
from database import DatabaseService


alias_router = APIRouter(prefix='/alias', tags=['Alias'])


@alias_router.get("")
async def get_aliases() -> list[Alias]:
    """Get all aliases.

    Returns:
        list[Alias]: List of all aliases.
    """
    return AliasService().get_aliases()


@alias_router.get("/{alias_id}")
async def get_alias(alias_id: str) -> Alias:
    """Get alias of a user.

    Args:
        alias_id (str): The user account.

    Raises:
        HTTPException: User doesn"t exist.

    Returns:
        Alias: List of aliases of the user.
    """
    db_virtual = DatabaseService(DatabaseName.VIRTUAL.value)
    email_alias = db_virtual.find_text(text=alias_id)
    if not email_alias:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Alias {alias_id} doesn't exist.")
    return AliasService().get_alias(email=alias_id) or {}


@alias_router.post("")
async def create_alias(user: Alias) -> Alias:
    """Create alias for a user.

    Args:
        user (Alias): The user to create alias for.

    Raises:
        HTTPException: User doen't exist.

    Returns:
        Alias: The newly alias.
    """
    db_virtual = DatabaseService(name=DatabaseName.VIRTUAL.value)
    email_alias = db_virtual.find_text(text=user.email_alias)
    if email_alias:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"The Alias {user.email_alias} already exist. Use PATCH to update alias.")
    alias_service = AliasService()
    alias_service.create_alias(recipients=user.email_recipient, alias=user.email_alias)
    return Alias(email_alias=user.email_alias, email_recipient=user.email_recipient)


@alias_router.patch("")
async def update_alias(user: Alias) -> Alias:
    """Update aliases of a user.

    Args:
        user (Alias): The user for which to update the alias.

    Raises:
        HTTPException: Alias doen't exist.

    Returns:
        Alias: The updated aliases.
    """
    db_virtual = DatabaseService(name=DatabaseName.VIRTUAL.value)
    email_alias = db_virtual.find_text(text=user.email_alias)
    if not email_alias:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Alias {user.email_alias} doesn't exist.")
    alias_service = AliasService()
    new_alias = alias_service.update_alias(recipients=user.email_recipient, alias=user.email_alias)
    return new_alias


@alias_router.delete("/{alias_id}", status_code=204)
async def delete_alias(alias_id: str):
    """Remove an alias.

    Args:
        alias_id (str): The alias to remove

    Raises:
        HTTPException: Alias doesn't exist.
    """
    db_virtual = DatabaseService(name=DatabaseName.VIRTUAL.value)
    email_alias = db_virtual.find_text(text=alias_id)
    if not email_alias:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The Alias {alias_id} doesn't exist.")
    db_virtual.remove(text=email_alias[0])
