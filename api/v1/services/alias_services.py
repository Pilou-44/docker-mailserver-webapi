"""Alias service."""
from database import DatabaseService
from schemas.email import Alias
from config import DatabaseName


class AliasService():
    """Alias class."""
    def __init__(self):
        self.db_virtual = DatabaseService(name=DatabaseName.VIRTUAL.value)

    def get_aliases(self) -> list[Alias]:
        """Get all aliases."""
        aliases = []
        foundaliasses = self.db_virtual.find(split=True)
        for alias in foundaliasses:
            recipents = alias[1].split(',')
            aliases.append(Alias(email_recipient=recipents, email_alias=alias[0]))
        return aliases

    def get_alias(self, email: str) -> Alias:
        """Get aliases of a user."""
        foundaliasses = self.db_virtual.find_text(text=email, split=True, find_in_column=True)
        if foundaliasses:
            alias = foundaliasses[0]
            recipents = alias[1].split(',')
            return Alias(email_recipient=recipents, email_alias=alias[0])
        return None

    def create_alias(self, alias: str, recipients: list[str]) -> Alias:
        """Create aliases for a user."""
        email_alias: list[list[str]] = self.db_virtual.find_text(text=alias, split=True, find_in_column=True)
        if not email_alias:
            recipients_str = ",".join(recipients)
            self.db_virtual.add(text=[alias, recipients_str])
            return Alias(email_alias=alias, email_recipient=recipients)

    def update_alias(self, alias: str, recipients: list[str]) -> Alias:
        """Update aliases for a user."""
        email_alias: list[list[str]] = self.db_virtual.find_text(text=alias, split=True, find_in_column=True)
        old_recipent = email_alias[0][1].split(',')
        old_recipent.extend(recipients)
        recipients_str = ",".join(list(set(old_recipent)))
        self.db_virtual.replace(text=[alias, recipients_str])
        return Alias(email_alias=alias, email_recipient=recipients_str.split(','))

    def remove_alias(self, alias: str):
        """Remove an alias."""
        email_alias = self.db_virtual.find_text(text=alias)
        if email_alias:
            self.db_virtual.remove(email_alias[0])
