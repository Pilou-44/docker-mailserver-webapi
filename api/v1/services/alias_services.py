from database import DatabaseService
from schemas.email import Alias
from config import DatabaseName


class AliasService():
    """as"""
    def __init__(self):
        self.db_virtual = DatabaseService(name=DatabaseName.VIRTUAL.value)

    def get_alias(self, email: str) -> list[Alias]:
        """ga"""
        aliases = []
        for alias in self.db_virtual.find_text(text=email, split=True):
            aliases.append(Alias(email_alias=alias))
        return aliases
