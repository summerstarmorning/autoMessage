---
name: auto-email-mode
description: Draft and send outbound emails with a local SMTP configuration. Use when the user wants Codex to prepare or send an email from the workspace without wiring a separate mail service first.
---

# Auto Email Mode

## Purpose

Use this skill when the user wants to send an email from Codex with a local SMTP account.
For Gmail, prefer App Password based SMTP unless the user explicitly asks for an OAuth Gmail API flow.
For QQ Mail, prefer the built-in SMTP service with a QQ Mail authorization code.

## Required environment variables

- `AUTO_EMAIL_SMTP_HOST`
- `AUTO_EMAIL_SMTP_PORT` (optional, defaults to `587`)
- `AUTO_EMAIL_SMTP_USER` (optional when the server allows anonymous auth)
- `AUTO_EMAIL_SMTP_PASSWORD` (optional when the server allows anonymous auth)
- `AUTO_EMAIL_FROM` (defaults to `AUTO_EMAIL_SMTP_USER` when omitted)
- `AUTO_EMAIL_USE_SSL` (optional, set to `1` or `true` for implicit SSL)
- `AUTO_EMAIL_PROVIDER` (optional, set to `gmail` to use Gmail defaults)

## QQ Mail notes

1. Log in to QQ Mail on the web.
2. Open settings and enable SMTP service.
3. Generate the QQ Mail authorization code.
4. Use `smtp.qq.com` with either:
   - port `465` and SSL, or
   - port `587` and STARTTLS.
5. Set `AUTO_EMAIL_PROVIDER=qq` so the script can fill the host and port defaults.

## Gmail notes

1. Turn on 2-Step Verification for the Google account.
2. Create an App Password for the script.
3. Use `smtp.gmail.com` with either:
   - port `587` and STARTTLS, or
   - port `465` and SSL.
4. Set `AUTO_EMAIL_PROVIDER=gmail` so the script can fill the host and port defaults.
5. If the sender uses Google Workspace and SMTP auth is blocked, move to Gmail API OAuth instead of retrying basic credential login.

## Workflow

1. Confirm the recipients, subject, and body content.
2. Ask whether the user wants a dry run or a real send if that is not already clear.
3. Run `scripts/send_email.py` with the provided arguments.
4. Report the recipient list, subject, and whether the message was sent or only validated.

## Examples

```powershell
python .\plugins\auto-email\scripts\send_email.py `
  --to "user@example.com" `
  --subject "Status Update" `
  --body "The nightly job completed successfully."
```

```powershell
python .\plugins\auto-email\scripts\send_email.py `
  --to "user@example.com" `
  --subject "Draft Only" `
  --body-file ".\drafts\mail.txt" `
  --dry-run
```
