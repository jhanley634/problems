#! /usr/bin/env _TYPER_STANDARD_TRACEBACK=1 python

from collections.abc import Generator
from email import policy
from email.message import EmailMessage
from email.parser import BytesParser
from imaplib import IMAP4_SSL
from pathlib import Path

import typer

from mail.imap_client import get_imap_client, select_inbox


def _get_email(eml_file: Path) -> EmailMessage:
    with eml_file.open("rb") as file:
        return BytesParser(policy=policy.default).parse(file)  # type: ignore


def fetch_emails_by_msg_id(client: IMAP4_SSL, msg_id: str) -> Generator[EmailMessage]:
    """Fetch email by message ID."""
    status, data = client.search(None, f'(HEADER Message-ID "{msg_id}")')
    assert "OK" == status, status
    assert data
    for num in data[0].split():
        _result, data = client.fetch(num, "(RFC822)")
        assert "OK" == status, status
        print(data)
        pair, _ = data
        _, hdrs = pair or (b"", b"")
        assert isinstance(hdrs, bytes)
        email_message = BytesParser(policy=policy.default).parsebytes(hdrs)  # type: ignore
        assert isinstance(email_message, EmailMessage)
        yield email_message


def show_chain(msg_id: str = "1E253999-EDC9-405C-94B3-CB91CFFBD5CE@gmail.com") -> None:
    """Reads a GMail inbox via IMAP.

    It chases any References: message IDs, recursively, to visit older messages.
    """
    print(msg_id)
    client = select_inbox(get_imap_client())

    visited_msg_ids = set()
    to_visit_msg_ids = {msg_id}

    while to_visit_msg_ids:
        current_msg_id = to_visit_msg_ids.pop()

        if current_msg_id in visited_msg_ids:
            continue

        visited_msg_ids.add(current_msg_id)

        for email_message in fetch_emails_by_msg_id(client, current_msg_id):
            print(f"Message-ID: {email_message['Message-Id']}")

            # Print subject or any other desired header
            print("Subject:", email_message.get("subject", "No Subject"))

            # Handle references and follow them recursively
            references = email_message.get_all("References", [])
            for reference in references:
                msg_ids = reference.split()
                for ref_msg_id in msg_ids:
                    if ref_msg_id not in visited_msg_ids:
                        to_visit_msg_ids.add(ref_msg_id)

        print("-" * 40)  # Separator line


if __name__ == "__main__":
    typer.run(show_chain)
