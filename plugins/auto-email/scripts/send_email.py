#!/usr/bin/env python3
"""Send an email through SMTP using local environment variables."""

from __future__ import annotations

import argparse
import mimetypes
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path


GMAIL_SMTP_HOST = "smtp.gmail.com"
GMAIL_SSL_PORT = 465
GMAIL_STARTTLS_PORT = 587
QQ_SMTP_HOST = "smtp.qq.com"
QQ_SSL_PORT = 465
QQ_STARTTLS_PORT = 587


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send an email through SMTP.")
    parser.add_argument("--to", action="append", required=True, help="Recipient address")
    parser.add_argument("--cc", action="append", default=[], help="CC address")
    parser.add_argument("--bcc", action="append", default=[], help="BCC address")
    parser.add_argument(
        "--attach",
        action="append",
        default=[],
        help="Path to a file attachment; repeat to attach multiple files",
    )
    parser.add_argument("--subject", required=True, help="Email subject")
    body_group = parser.add_mutually_exclusive_group(required=True)
    body_group.add_argument("--body", help="Inline email body")
    body_group.add_argument("--body-file", help="Path to a text file for the body")
    html_group = parser.add_mutually_exclusive_group()
    html_group.add_argument("--html-body", help="Inline HTML body")
    html_group.add_argument("--html-body-file", help="Path to an HTML file for the body")
    parser.add_argument("--dry-run", action="store_true", help="Validate without sending")
    return parser.parse_args()


def env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


def env_value(name: str) -> str:
    return os.getenv(name, "").strip()


def provider_name() -> str:
    return env_value("AUTO_EMAIL_PROVIDER").lower()


def read_body(args: argparse.Namespace) -> str:
    if args.body is not None:
        return args.body
    return Path(args.body_file).read_text(encoding="utf-8")


def read_html_body(args: argparse.Namespace) -> str | None:
    if args.html_body is not None:
        return args.html_body
    if args.html_body_file is not None:
        return Path(args.html_body_file).read_text(encoding="utf-8")
    return None


def require_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def attach_files(message: EmailMessage, attachments: list[str]) -> None:
    for raw_path in attachments:
        path = Path(raw_path)
        if not path.is_file():
            raise SystemExit(f"Attachment file not found: {path}")

        mime_type, _ = mimetypes.guess_type(path.name)
        if mime_type:
            maintype, subtype = mime_type.split("/", 1)
        else:
            maintype, subtype = "application", "octet-stream"

        message.add_attachment(
            path.read_bytes(),
            maintype=maintype,
            subtype=subtype,
            filename=path.name,
        )


def build_message(args: argparse.Namespace) -> EmailMessage:
    sender = env_value("AUTO_EMAIL_FROM") or env_value("AUTO_EMAIL_SMTP_USER")
    if not sender:
        raise SystemExit(
            "Missing sender address. Set AUTO_EMAIL_FROM or AUTO_EMAIL_SMTP_USER."
        )

    message = EmailMessage()
    message["From"] = sender
    message["To"] = ", ".join(args.to)
    if args.cc:
        message["Cc"] = ", ".join(args.cc)
    message["Subject"] = args.subject
    plain_body = read_body(args)
    html_body = read_html_body(args)
    message.set_content(plain_body)
    if html_body is not None:
        message.add_alternative(html_body, subtype="html")
    attach_files(message, args.attach)
    return message


def connect():
    provider = provider_name()
    use_ssl = env_flag("AUTO_EMAIL_USE_SSL")
    default_host = ""
    if provider == "gmail":
        default_host = GMAIL_SMTP_HOST
    elif provider == "qq":
        default_host = QQ_SMTP_HOST

    host = env_value("AUTO_EMAIL_SMTP_HOST") or default_host
    if not host:
        raise SystemExit(
            "Missing SMTP host. Set AUTO_EMAIL_SMTP_HOST or AUTO_EMAIL_PROVIDER."
        )

    if env_value("AUTO_EMAIL_SMTP_PORT"):
        port = int(env_value("AUTO_EMAIL_SMTP_PORT"))
    elif provider == "gmail":
        port = GMAIL_SSL_PORT if use_ssl else GMAIL_STARTTLS_PORT
    elif provider == "qq":
        port = QQ_SSL_PORT if use_ssl else QQ_STARTTLS_PORT
    else:
        port = 587

    username = env_value("AUTO_EMAIL_SMTP_USER")
    password = os.getenv("AUTO_EMAIL_SMTP_PASSWORD", "")

    if use_ssl:
        server = smtplib.SMTP_SSL(host, port, context=ssl.create_default_context())
    else:
        server = smtplib.SMTP(host, port)
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()

    if username:
        server.login(username, password)
    return server


def main() -> None:
    args = parse_args()
    message = build_message(args)
    recipients = args.to + args.cc + args.bcc
    provider = provider_name() or "custom"

    if args.dry_run:
        print("Dry run successful.")
        print(f"Provider: {provider}")
        print(f"From: {message['From']}")
        print(f"To: {message['To']}")
        if args.cc:
            print(f"Cc: {message['Cc']}")
        print(f"Subject: {message['Subject']}")
        print(f"HTML body: {'yes' if read_html_body(args) is not None else 'no'}")
        print(f"Attachments: {len(args.attach)}")
        print(f"Recipients counted for send: {len(recipients)}")
        return

    with connect() as server:
        server.send_message(message, to_addrs=recipients)

    print("Email sent successfully.")
    print(f"Provider: {provider}")
    print(f"To: {message['To']}")
    if args.cc:
        print(f"Cc: {message['Cc']}")
    print(f"Subject: {message['Subject']}")
    print(f"HTML body: {'yes' if read_html_body(args) is not None else 'no'}")
    print(f"Attachments: {len(args.attach)}")


if __name__ == "__main__":
    main()
