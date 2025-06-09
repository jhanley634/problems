from imaplib import IMAP4_SSL
import os


def get_imap_client() -> IMAP4_SSL:
    server = os.getenv("GMAIL_IMAP_SERVER", "imap.gmail.com")
    user = os.getenv("GMAIL_USER", "jhanley741@gmail.com")
    pw = os.environ["GMAIL_PASSWORD"]
    client = IMAP4_SSL(server)
    client.login(user, pw)
    client.noop()
    return client


def select_inbox(client: IMAP4_SSL, inbox_name: str = "INBOX") -> IMAP4_SSL:
    status, data = client.select(inbox_name)
    assert "OK" == status, status
    data0 = data[0] or b""
    num_msgs = int(data0.decode())
    assert num_msgs > 0, num_msgs
    return client
