#! /usr/bin/env python

import imaplib
import os


def read_recent_email() -> None:
    server = os.getenv("GMAIL_IMAP_SERVER", "imap.gmail.com")
    user = os.getenv("GMAIL_USER", "jhanley741@gmail.com")
    pw = os.environ["GMAIL_PASSWORD"]
    client = imaplib.IMAP4_SSL(server)
    client.login(user, pw)
    client.noop()

    status, payload = client.select("INBOX")
    assert "OK" == status, status
    payload0: bytes = payload[0] or b""
    num_msgs = int(payload0.decode())
    print(num_msgs)

    client.close()
    client.logout()


if __name__ == "__main__":
    read_recent_email()
