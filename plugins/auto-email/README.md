# Auto Email Plugin

This plugin now includes Gmail and QQ Mail SMTP workflows.

## Gmail setup

Google's current official guidance supports sending mail through `smtp.gmail.com`.
Common client settings are:

- `smtp.gmail.com`
- port `587` with TLS/STARTTLS, or
- port `465` with SSL

For account-password based access, Google requires 2-Step Verification and an App Password for desktop or script-style clients.

If you are using a Google Workspace account instead of a personal Gmail account, Google documents tighter third-party app restrictions as of May 1, 2025. If SMTP auth with an app password is rejected on Workspace, switch this plugin to an OAuth Gmail API flow instead of continuing to troubleshoot basic username/password login.

Official references:

- https://support.google.com/accounts/answer/2461835
- https://support.google.com/a/answer/176600
- https://developers.google.com/gmail/api/guides/sending

## Quick start

### Option 1: Persist Gmail env vars

```powershell
.\plugins\auto-email\scripts\setup_gmail_env.ps1 `
  -GmailAddress "your.name@gmail.com" `
  -AppPassword "your-16-char-app-password"
```

### Option 2: Session-only test

```powershell
$env:AUTO_EMAIL_PROVIDER = "gmail"
$env:AUTO_EMAIL_SMTP_HOST = "smtp.gmail.com"
$env:AUTO_EMAIL_SMTP_PORT = "587"
$env:AUTO_EMAIL_SMTP_USER = "your.name@gmail.com"
$env:AUTO_EMAIL_SMTP_PASSWORD = "your-16-char-app-password"
$env:AUTO_EMAIL_FROM = "your.name@gmail.com"
$env:AUTO_EMAIL_USE_SSL = "false"
```

## Send a test mail

```powershell
python .\plugins\auto-email\scripts\send_email.py `
  --to "recipient@example.com" `
  --subject "Gmail SMTP test" `
  --body "This message was sent from the auto-email plugin."
```

## Dry run

```powershell
python .\plugins\auto-email\scripts\send_email.py `
  --to "recipient@example.com" `
  --subject "Draft only" `
  --body "This is only a dry run." `
  --dry-run
```

## Gmail API option

If you later want OAuth-based sending instead of SMTP with an App Password, the Gmail API is the next step. The current SMTP workflow is simpler for a local automation plugin and does not require building an OAuth consent flow first.

## QQ Mail setup

QQ Mail commonly uses:

- `smtp.qq.com`
- port `465` with SSL, or
- port `587` with STARTTLS

QQ Mail does not use your QQ login password for SMTP clients. You need to enable SMTP service in QQ Mail settings and use the generated authorization code.

### Persist QQ Mail env vars

```powershell
.\plugins\auto-email\scripts\setup_qq_env.ps1 `
  -QqAddress "summerstarmorning@qq.com" `
  -AuthCode "your-qq-mail-auth-code"
```

### Session-only test

```powershell
$env:AUTO_EMAIL_PROVIDER = "qq"
$env:AUTO_EMAIL_SMTP_HOST = "smtp.qq.com"
$env:AUTO_EMAIL_SMTP_PORT = "465"
$env:AUTO_EMAIL_SMTP_USER = "summerstarmorning@qq.com"
$env:AUTO_EMAIL_SMTP_PASSWORD = "your-qq-mail-auth-code"
$env:AUTO_EMAIL_FROM = "summerstarmorning@qq.com"
$env:AUTO_EMAIL_USE_SSL = "true"
```

### Send a QQ Mail test message

```powershell
python .\plugins\auto-email\scripts\send_email.py `
  --to "recipient@example.com" `
  --subject "QQ Mail SMTP test" `
  --body "This message was sent from the auto-email plugin."
```

## Timed love greeting profile

The timed greeting script now reads its writing style from:

- `.\plugins\auto-email\data\love_greeting_profile.json`

You can edit that file to change:

- nicknames
- signatures
- weekday tone
- weekend extra lines
- holiday overrides
- custom special dates such as birthdays or anniversaries

The automations already call `send_love_greeting.py`, so profile changes take effect on the next scheduled run without recreating the tasks.

## GitHub Actions online version

If you want the messages to send even when your own computer is off, use:

- `.\.github\workflows\love-mail.yml`

This workflow is designed for GitHub Actions and runs three times per day in Beijing time by using UTC cron values:

- `07:00` China time -> `23:00` UTC on the previous day
- `13:00` China time -> `05:00` UTC
- `23:00` China time -> `15:00` UTC

Required repository secrets:

- `QQ_SMTP_USER`
- `QQ_SMTP_PASSWORD`
- `LOVE_MAIL_TO`

Recommended `LOVE_MAIL_TO` value for your current use case:

- `3308029362@qq.com`

The greeting generator will still use `Asia/Shanghai` for weekday, weekend, and holiday logic.
