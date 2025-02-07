from api.v1.utils import EmailNotFoundException
from database import DatabaseService
from schemas.email import Restriction
from config import DatabaseName


class RestrictionService():
    """as"""
    def __init__(self):
        self.db_account = DatabaseService(name=DatabaseName.ACCOUNTS.value)
        self.db_access_send = DatabaseService(name=DatabaseName.ACCESS_SEND.value)
        self.db_access_recv = DatabaseService(name=DatabaseName.ACCESS_RECEIVE.value)

    def get_restriction(self, email: str) -> Restriction:
        """ga"""
        if not self.db_account.find_text(text=email):
            raise EmailNotFoundException(f"Mail account {email} does not exist")
        get_acces_send = self.db_access_send.find_text(email)
        get_acces_rcv = self.db_access_recv.find_text(email)
        return Restriction(send=len(get_acces_send) > 0, receive=len(get_acces_rcv) > 0)
