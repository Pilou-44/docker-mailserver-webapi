import os
from pathlib import Path
from config import DatabaseName


class DatabaseService:
    """d"""
    def __init__(self, name):
        self.config_path = os.getenv("WEB_API_DMS_CONFIG_PATH")
        self.database_name = name
        self.database_path = Path(self.config_path) / Path(self.database_name)
        if not self.database_path.exists():
            _ = self.database_path.write_bytes(b"")

    def get_delimiter(self) -> str:
        """g"""
        match self.database_name:
            case DatabaseName.QUOTA.value:
                return ':'
            case (DatabaseName.ACCOUNTS.value | DatabaseName.DOVECOT_MASTERS.value):
                return '|'
            case (DatabaseName.RELAY.value | DatabaseName.PASSWD.value | DatabaseName.VIRTUAL.value):
                return ' '
            case (DatabaseName.ACCESS_SEND.value | DatabaseName.ACCESS_RECEIVE.value):
                return '\t\t'
            case _:
                raise ValueError(f"Unsupported DB: {self.database_name}")

    def find(self, split: bool = False) -> list[str] | list[list[str]]:
        """f"""
        filedata = self.database_path.read_bytes().splitlines()
        filedata_without_comment = [x.decode() for x in filedata if not x.startswith(b'#')]
        if split:
            delim = self.get_delimiter()
            return [x.split(delim) for x in filedata_without_comment if x]
        return filedata_without_comment

    def find_text(self, text: str, split: bool = False, find_in_column: bool = False) -> list[str] | list[list[str]]:
        """f"""
        matches = []
        filedata = self.database_path.read_bytes().splitlines()
        filedata_without_comment = [x.decode() for x in filedata if not x.startswith(b'#')]
        for line in filedata_without_comment:
            if split and find_in_column and text in line.split(self.get_delimiter()):
                matches.append(line.split(self.get_delimiter()))
                continue
            if text in line:
                matches.append(line)
        return matches

    def add(self, text: list[str]):
        """a"""
        delim = self.get_delimiter()
        with self.database_path.open(mode="+a") as f:
            f.write(f"{delim}".join(text) + '\n')

    def replace(self, text: list[str]):
        """a"""
        delim = self.get_delimiter()
        filedata = self.database_path.read_text().splitlines(keepends=True)
        with self.database_path.open(mode="+w") as f:
            for line in filedata:
                if line.startswith(text[0] + delim):
                    line = f"{delim}".join(text) + '\n'
                f.write(line)

    def remove(self, text: str):
        """a"""
        filedata = self.database_path.read_text().splitlines(keepends=True)
        with self.database_path.open(mode="+w") as f:
            for line in filedata:
                if line.strip() == text:
                    continue
                f.write(line)
