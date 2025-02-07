import subprocess
import crypt

from config import DatabaseName
from database import DatabaseService


class DovecotService():
    """as"""
    def __init__(self):
        self.db_virtual = DatabaseService(name=DatabaseName.DOVECOT_MASTERS.value)

    def get_quota_used(self, email: str) -> tuple[float, float]:
        """ga"""

        command = f"doveadm quota get -u {email}" + " | tail +2 | awk '{ if ($3 == \"STORAGE\") { print $4\" \"$5\" \"$6 } }'"
        process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
        out, _ = process.communicate(command)
        if out:
            return (float(out.partition(" ")[0]), float(out.partition(" ")[-1]))
        return (float(-1), 0)

    def create_password_hash(self, password: str) -> str:
        """p"""
        hashed_password = crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))
        return "{SHA512-CRYPT}" + hashed_password
