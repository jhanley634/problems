#! /usr/bin/env python


from email.message import Message
from imaplib import IMAP4_SSL
import email

from mail.imap_client import get_imap_client, select_inbox


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
Date: {date}
Message-ID: {msg.get("Message-ID")}
"""


if __name__ == "__main__":
    display_unread_messages(select_inbox(get_imap_client()))
