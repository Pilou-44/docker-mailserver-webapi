"""Postfix service."""
import re
import subprocess
from pathlib import Path

from api.v1.utils import RestrictionAccess


class PostfixService():
    """Postfix class"""

    def update_postfix_restriction(self, access: RestrictionAccess) -> bool:
        """Update postfix restriction by update main.cf file"""
        if access.value == "send":
            check = "check_sender_access"
            postfix_option = "smtpd_sender_restrictions"
        else:
            check = "check_recipient_access"
            postfix_option = "smtpd_recipient_restrictions"

        string_to_be_added = f"{check} texthash:/tmp/docker-mailserver/postfix-{access.value}-access.cf"
        postfix_config_path = "/etc/postfix/main.cf"

        config_content = Path(postfix_config_path).read_text(encoding='utf-8')

        if string_to_be_added not in config_content:
            updated_content = re.sub(rf"^({postfix_option} =)(.*)", rf"\1 {string_to_be_added},\2", config_content, flags=re.MULTILINE)

            _ = Path(postfix_config_path).write_text(data=updated_content, encoding='utf-8')

        subprocess.run(["service", "postfix", "reload"], check=True)

        command = "systemctl reload postfix"
        _ = subprocess.run(command, check=True)
        return True
