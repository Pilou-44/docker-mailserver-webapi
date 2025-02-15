"""Fail2ban"""
from fastapi import APIRouter

from api.v1.services.fail2ban_services import Fail2banService
from schemas.fail2ban import Fail2banJail

fail2ban_router = APIRouter(prefix='/fail2ban', tags=['Fail2ban'])


@fail2ban_router.get("")
async def get_banned(name: str | None = None) -> list[Fail2banJail]:
    """Get all fail2ban jail and banned items."""
    return Fail2banService().get_jail(name=name)


@fail2ban_router.post("/ban")
async def banned_ip(ip: str) -> list[Fail2banJail]:
    """Ban an IP in the 'custom' jail.

    Args:
        ip (str): The IP to ban.

    Returns:
        list[Fail2banJail]: The updated jail.
    """
    return Fail2banService().ban_ip(ip_addr=ip)


@fail2ban_router.post("/unban")
async def unbanned_ip(ip: str) -> list[Fail2banJail]:
    """Unabn an IP fro the 'custom' jail.

    Args:
        ip (str): The IP to unban.

    Returns:
        list[Fail2banJail]: The updated jail.
    """
    return Fail2banService().unban_ip(ip_addr=ip)
