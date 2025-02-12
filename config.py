from enum import Enum


class DatabaseName(Enum):
    ACCOUNTS = "postfix-accounts.cf"
    ACCESS_SEND = "postfix-send-access.cf"
    ACCESS_RECEIVE = "postfix-receive-access.cf"
    DOVECOT_MASTERS = "dovecot-masters.cf"
    QUOTA = "dovecot-quotas.cf"
    VIRTUAL = "postfix-virtual.cf"
    PASSWD = "postfix-sasl-password.cf"
    RELAY = "postfix-relaymap.cf"
