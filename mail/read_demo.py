#! /usr/bin/env python


from email.message import Message
from imaplib import IMAP4_SSL
import email
import os


def _get_imap_client() -> IMAP4_SSL:
    server = os.getenv("GMAIL_IMAP_SERVER", "imap.gmail.com")
    user = os.getenv("GMAIL_USER", "jhanley741@gmail.com")
    pw = os.environ["GMAIL_PASSWORD"]
    client = IMAP4_SSL(server)
    client.login(user, pw)
    client.noop()
    return client


def _select_inbox(client: IMAP4_SSL, inbox_name: str = "INBOX") -> IMAP4_SSL:
    status, data = client.select(inbox_name)
    assert "OK" == status, status
    data0 = data[0] or b""
    num_msgs = int(data0.decode())
    assert num_msgs > 0, num_msgs
    return client


def display_unread_messages(client: IMAP4_SSL) -> None:

    try:
        status, data = client.search(None, "UNSEEN")
        assert "OK" == status, status
        # print(data)  # e.g. [b'10138 10139']
        unseen_msg_uids = data[0].split()
        print(f"Found {len(unseen_msg_uids)} unread\n")

        for msg_uid in unseen_msg_uids:
            status, data = client.fetch(msg_uid, "(RFC822.HEADER)")
            assert "OK" == status, status
            pair, _ = data
            _, hdrs = pair or (b"", b"")
            assert isinstance(hdrs, bytes), hdrs
            msg = email.message_from_bytes(hdrs)
            print(_summarize_headers(msg))

    finally:
        client.close()
        client.logout()


def _summarize_headers(msg: Message) -> str:
    subject = msg.get("Subject", "No Subject")
    from_ = msg.get("From", "Unknown Sender")
    date = msg.get("Date", "No Date")

    return f"""From: {from_}
Subject: {subject}
Date: {date}\n"""


if __name__ == "__main__":
    display_unread_messages(_select_inbox(_get_imap_client()))
