"""Restriction service"""
from api.v1.services.postfix_services import PostfixService
from api.v1.utils import EmailNotFoundException, RestrictionAccess
from database import DatabaseService
from schemas.email import Restriction
from config import DatabaseName


class RestrictionService():
    """Restriction class"""
    def __init__(self):
        self.db_account = DatabaseService(name=DatabaseName.ACCOUNTS.value)
        self.db_access_send = DatabaseService(name=DatabaseName.ACCESS_SEND.value)
        self.db_access_recv = DatabaseService(name=DatabaseName.ACCESS_RECEIVE.value)
        self.postfix_service = PostfixService()

    def get_restriction(self, email: str) -> Restriction:
        """Get the restriction for a user."""
        if not self.db_account.find_text(text=email):
            raise EmailNotFoundException(f"Mail account {email} does not exist")
        get_acces_send = self.db_access_send.find_text(email)
        get_acces_rcv = self.db_access_recv.find_text(email)
        return Restriction(send=len(get_acces_send) > 0, receive=len(get_acces_rcv) > 0)

    def update_restriction(self, email: str, acces: RestrictionAccess) -> Restriction:
        """Update the restriction for a user."""
        if not self.db_account.find_text(text=email):
            raise EmailNotFoundException(f"Mail account {email} does not exist")

        existing_restriction = self.get_restriction(email)
        access_send = existing_restriction.send
        access_recv = existing_restriction.receive
        match acces:
            case RestrictionAccess.SEND:
                if not existing_restriction.send:
                    self.db_access_send.add(text=[email, "REJECT"])
                    access_send = True

            case RestrictionAccess.RECV:
                if not existing_restriction.receive:
                    self.db_access_recv.add(text=[email, "REJECT"])
                    access_recv = True
            case _:
                raise ValueError("Invalid access.")

        self.postfix_service.update_postfix_restriction(acces)
        return Restriction(send=access_send, receive=access_recv)

    def remove_restriction(self, email: str, acces: RestrictionAccess) -> Restriction:
        """Remove a restriction for a user."""
        if not self.db_account.find_text(text=email):
            raise EmailNotFoundException(f"Mail account {email} does not exist")

        get_access_send = self.db_access_send.find_text(text=email)
        get_access_recv = self.db_access_recv.find_text(text=email)
        access_send = len(get_access_send) > 0
        access_recv = len(get_access_recv) > 0
        match acces:
            case RestrictionAccess.SEND:
                if access_send:
                    self.db_access_send.remove(text=[get_access_send[0]])
                    access_send = False

            case RestrictionAccess.RECV:
                if access_recv:
                    self.db_access_recv.remove(text=[get_access_recv[0]])
                    access_recv = False
            case _:
                raise ValueError("Invalid access.")
        return Restriction(send=access_send, receive=access_recv)
