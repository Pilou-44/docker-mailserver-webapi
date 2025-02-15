""""Email"""
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from api.v1.services.alias_services import AliasService
from api.v1.services.dovecot_services import DovecotService
from api.v1.services.quota_services import QuotaService
from api.v1.services.restriction_services import RestrictionService
from schemas.email import Email, EmailCreate, Restriction, Quota
from config import DatabaseName
from database import DatabaseService


email_router = APIRouter(prefix='/email', tags=['Email'])


@email_router.get("")
async def get_accounts() -> list[Email]:
    """Get all users accounts.

    Returns:
        list[Email]: List of all the users.
    """
    accounts: list[Email] = []
    db = DatabaseService(DatabaseName.ACCOUNTS.value)
    all_acc = db.find(split=True)
    for user, password in all_acc:
        alias = AliasService().get_alias(user)
        quota = QuotaService().get_quota(user)
        restriction = RestrictionService().get_restriction(user)
        if alias:
            alias = [alias]
        else:
            alias = []

        accounts.append(Email(username=user, password=password, alias=alias, quota=quota, restriction=restriction))
    return accounts


@email_router.get("/{email_id}")
async def get_account(email_id: str) -> Email:
    """Get details of an user account.

    Args:
        email_id (str): User to get info from.

    Raises:
        HTTPException: Email doesn't exist.

    Returns:
        Email: The user account info.
    """
    db = DatabaseService(DatabaseName.ACCOUNTS.value)
    all_acc = db.find(split=True)
    for user, password in all_acc:
        alias = AliasService().get_alias(user)
        if alias:
            alias = [alias]
        else:
            alias = []
        quota = QuotaService().get_quota(user)
        restriction = RestrictionService().get_restriction(user)
        if user == email_id:
            return Email(username=user, password=password, alias=alias, quota=quota, restriction=restriction)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {email_id} not found")


@email_router.post("")
async def create_account(user: EmailCreate) -> Email:
    """Creation of a new user account.

    Args:
        user (EmailCreate): The account to create.

    Raises:
        HTTPException: Email already exist.

    Returns:
        Email: The newly account.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    if db_account.find_text(text=user.email):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {user.email} already exist")

    hashed_password = DovecotService().create_password_hash(user.password)
    db_account.add(text=[user.email, hashed_password])
    return Email(username=user.email, password=hashed_password, alias=[], quota=Quota(quota_percent=0.0, quota=0, quota_used=0), restriction=Restriction(send=False, receive=False))


@email_router.patch("")
async def update_password(user: EmailCreate) -> Email:
    """Update password of an email account.

    Args:
        user (EmailCreate): The User to update.

    Raises:
        HTTPException: Email doesn't exist.

    Returns:
        Email: The new Email object.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    if not db_account.find_text(text=user.email):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {user.email} does not exist")

    hashed_password = DovecotService().create_password_hash(user.password)
    db_account.replace(text=[user.email, hashed_password])
    return Email(username=user.email, password=hashed_password, alias=[], quota=Quota(quota_percent=0.0, quota=0, quota_used=0), restriction=Restriction(send=False, receive=False))


@email_router.delete("/{email_id}", status_code=204)
async def delete_account(email_id: str):
    """Delete an email account.

    Args:
        email_id (str): The email address.

    Raises:
        HTTPException: Email doesn't exist.
    """
    db_account = DatabaseService(DatabaseName.ACCOUNTS.value)
    user = db_account.find_text(text=email_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Mail account {email_id} does not exist")
    db_account.remove(text=user[0])
