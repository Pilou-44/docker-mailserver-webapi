"""Fail2ban service (sqlite3)"""
import os
import sqlite3
from datetime import datetime
from pathlib import Path

from fastapi import status
from fastapi.exceptions import HTTPException

from schemas.fail2ban import Fail2banJail


class Fail2banService():
    """Fail2ban class"""
    def __init__(self):
        fail2ban_enable = os.getenv("ENABLE_FAIL2BAN", "0") == "1"
        if not fail2ban_enable:
            raise HTTPException(detail="Fail2ban is not running. Ensure you've included 'ENABLE_FAIL2BAN' in your compose file", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        if not os.getenv("WEB_API_FAIL2BAN_SQLITE_PATH"):
            raise HTTPException(detail="WEB_API_FAIL2BAN_SQLITE_PATH not set.", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        try:
            self.db_fail2ban_path = Path(os.getenv("WEB_API_FAIL2BAN_SQLITE_PATH"))
        except FileNotFoundError as fe:
            raise HTTPException(detail=f"Unable to open fail2ban database in {self.db_fail2ban_path}", status_code=status.HTTP_503_SERVICE_UNAVAILABLE) from fe

    def get_jail(self, name: str | None = None) -> list[Fail2banJail]:
        """Get all jail aor specific by name."""
        query_where = "WHERE jail = ?" if name else " "
        query_select_jail = f"""
            SELECT
                jail AS name,
                SUM(CASE WHEN (timeofban + bantime) > CAST(STRFTIME('%s', 'now') as INTEGER) THEN 1 ELSE 0 END) as 'currentlyBanned',
                COUNT(0) as 'totalBanned',
                GROUP_CONCAT(ip, ',') as 'bannedIps'
            FROM bips
            {query_where}
            GROUP BY jail;
        """

        fail2ban_con = sqlite3.connect(self.db_fail2ban_path, uri=True)
        cursor = fail2ban_con.cursor()

        # Execute query with or without filtering by `name`
        if name:
            cursor.execute(query_select_jail, (name,))
        else:
            cursor.execute(query_select_jail)

        results = cursor.fetchall()

        # Convert to `Fail2banJail` objects
        fail2ban_jails = [
            Fail2banJail(
                name=row[0],  # name
                currently_banned=row[1],  # currently_banned
                total_banned=row[2],  # total_banned
                banned_ips=row[3].split(",") if row[3] else []  # banned_ips as list
            )
            for row in results
        ]

        fail2ban_con.close()
        return fail2ban_jails

    def ban_ip(self, ip_addr: str) -> list[Fail2banJail]:
        """Ban IP (add in 'custom' jail)"""
        fail2ban_con = sqlite3.connect(self.db_fail2ban_path)
        cursor = fail2ban_con.cursor()

        # Get the current timestamp
        time_of_ban = int(datetime.now().timestamp())

        cursor.execute(
            """INSERT OR IGNORE INTO bips (jail, ip, timeofban, bantime) VALUES (?, ?, ?, ?)""",
            ("custom", ip_addr, time_of_ban, 10800)
        )

        fail2ban_con.commit()
        fail2ban_con.close()
        return self.get_jail(name='custom')

    def unban_ip(self, ip_addr: str) -> list[Fail2banJail]:
        """Unban IP (remove from 'custom' jail)"""
        fail2ban_con = sqlite3.connect(self.db_fail2ban_path)
        cursor = fail2ban_con.cursor()

        cursor.execute(
            "DELETE FROM bips WHERE jail = ? AND ip = ?",
            ('custom', ip_addr)
        )

        fail2ban_con.commit()
        fail2ban_con.close()
        return self.get_jail(name='custom')
