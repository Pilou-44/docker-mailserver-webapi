"""Dovecot service."""
import os
import subprocess
import crypt

from config import DatabaseName
from database import DatabaseService


class DovecotService():
    """Dovecot class"""
    def __init__(self):
        self.db_virtual = DatabaseService(name=DatabaseName.DOVECOT_MASTERS.value)

    def get_quota_used(self, email: str) -> tuple[float, float]:
        """retreive quota with dovecot for a user."""
        dockerexec = os.getenv('WEB_API_MAILSERVER_CONTAINER_NAME')
        if dockerexec:
            dockerexec += " "
        command = f"{dockerexec}doveadm quota get -u {email}" + " | tail +2 | awk '{ if ($3 == \"STORAGE\") { print $4\" \"$5\" \"$6 } }'"
        process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        out, _ = process.communicate(command)
        if out:
            return (float(out.partition(" ")[0]), float(out.partition(" ")[-1]))
        return (float(-1), 0)

    def create_password_hash(self, password: str) -> str:
        """Create hashed password (sha512) for a user."""
        hashed_password = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
        return "{SHA512-CRYPT}" + hashed_password
