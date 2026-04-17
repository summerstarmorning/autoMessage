# n8n Cloud Online Plan

This folder contains the cloud-first version of the daily greeting flow.

## Why n8n Cloud

This is the best fit for your requirement that messages still send when your own computer is off:

- n8n Cloud runs workflows on n8n's servers
- the Schedule Trigger node runs workflows at fixed times
- the Send Email node supports SMTP and HTML email
- n8n Cloud lets you set the instance timezone
- workflows can be imported and exported as JSON

Official docs:

- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.scheduletrigger/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.sendemail/
- https://docs.n8n.io/integrations/builtin/credentials/sendemail/
- https://docs.n8n.io/manage-cloud/set-cloud-timezone/
- https://docs.n8n.io/workflows/export-import/

## Recommended setup

Create 3 workflows in n8n Cloud:

1. Morning Love Mail
2. Noon Love Mail
3. Night Love Mail

Each workflow should contain:

1. `Schedule Trigger`
2. `Code`
3. `Send Email`

## Timezone

Set your n8n Cloud timezone to `Asia/Shanghai`.

## SMTP credential

Create a `Send Email` SMTP credential with:

- Host: `smtp.qq.com`
- Port: `465`
- SSL/TLS: `ON`
- User: your QQ mailbox
- Password: your QQ mailbox authorization code

Do not use your QQ login password.

## Schedule Trigger settings

### Morning

- Trigger interval: `Weeks`
- Weekdays: all days
- Hour: `7`
- Minute: `0`

### Noon

- Trigger interval: `Weeks`
- Weekdays: all days
- Hour: `13`
- Minute: `0`

### Night

- Trigger interval: `Weeks`
- Weekdays: all days
- Hour: `23`
- Minute: `0`

## Code node

Paste the contents of `love_greeting_code.js` into the `Code` node.

Then set these inputs at the top of the code:

- `slot`: `morning`, `noon`, or `night`
- `toEmail`: `3308029362@qq.com`

If you want to customize names, signatures, special dates, or the writing style, edit the arrays and objects in that file.

## Send Email node

Recommended configuration:

- Operation: `Send`
- From Email: your QQ email
- To Email: `={{ $json.toEmail }}`
- Subject: `={{ $json.subject }}`
- Email Format: `Both`
- Text: `={{ $json.plain }}`
- HTML: `={{ $json.html }}`
- Append n8n Attribution: `OFF`

## Notes

- This runs even when your own PC is off, because execution happens in n8n Cloud.
- It still depends on your n8n Cloud account being active and your QQ SMTP authorization code remaining valid.
- Because you previously exposed a QQ authorization code in chat, rotate it before using it in n8n Cloud.
