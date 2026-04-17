#!/usr/bin/env python3
"""Generate and send a timed romantic greeting email with profile-based variations."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
from email.message import EmailMessage
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

import send_email


PROFILE_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "love_greeting_profile.json"
)


DEFAULT_HOLIDAYS = {
    "01-01": {
        "name": "元旦",
        "style": "新年",
        "mood": "新一年的第一份偏爱先留给你。",
    },
    "02-14": {
        "name": "情人节",
        "style": "浪漫",
        "mood": "今天就该理直气壮地多偏爱你一点。",
    },
    "03-08": {
        "name": "女神节",
        "style": "宠溺",
        "mood": "今天的你就负责漂亮和开心，别的交给我来夸。",
    },
    "05-20": {
        "name": "520",
        "style": "表白",
        "mood": "这种日子就适合认真告诉你，我是真的很喜欢你。",
    },
    "06-01": {
        "name": "儿童节",
        "style": "俏皮",
        "mood": "今天允许你当一天被宠着的小朋友。",
    },
    "10-01": {
        "name": "国庆节",
        "style": "假期",
        "mood": "假期要开心一点，也要记得被我惦记着。",
    },
    "12-24": {
        "name": "平安夜",
        "style": "温柔",
        "mood": "今晚想把平安和偏爱一起打包给你。",
    },
    "12-25": {
        "name": "圣诞节",
        "style": "礼物感",
        "mood": "今天的你像被节日特地偏爱了一下。",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a timed love greeting email.")
    parser.add_argument("--slot", choices=["morning", "noon", "night"], required=True)
    parser.add_argument("--to", required=True, help="Recipient address")
    parser.add_argument(
        "--date",
        help="Override local date in YYYY-MM-DD for testing variant rotation",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def current_timezone() -> ZoneInfo:
    timezone_name = send_email.env_value("AUTO_EMAIL_TIMEZONE") or "Asia/Shanghai"
    try:
        return ZoneInfo(timezone_name)
    except Exception as exc:
        raise SystemExit(f"Invalid AUTO_EMAIL_TIMEZONE value: {timezone_name}") from exc


def resolve_date(date_text: str | None) -> dt.date:
    if date_text:
        return dt.date.fromisoformat(date_text)
    return dt.datetime.now(current_timezone()).date()


def load_profile() -> dict:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def build_rng(send_date: dt.date, slot: str) -> random.Random:
    return random.Random(f"love-mail:{send_date.isoformat()}:{slot}")


def choose(rng: random.Random, values: list[str]) -> str:
    return values[rng.randrange(len(values))]


def pick_unique(rng: random.Random, values: list[str], count: int) -> list[str]:
    if len(values) <= count:
        return list(values)
    return rng.sample(values, count)


def holiday_for_date(profile: dict, send_date: dt.date) -> dict | None:
    date_key = send_date.strftime("%m-%d")
    custom = profile.get("special_dates", {})
    if date_key in custom:
        payload = dict(custom[date_key])
        payload.setdefault("name", date_key)
        return payload
    if date_key in DEFAULT_HOLIDAYS:
        return dict(DEFAULT_HOLIDAYS[date_key])
    return None


def slot_config(profile: dict, slot: str) -> dict:
    return profile["slot_styles"][slot]


def day_context(profile: dict, send_date: dt.date) -> dict:
    holiday = holiday_for_date(profile, send_date)
    if holiday is not None:
        return {"kind": "holiday", "label": holiday["name"], "data": holiday}
    if send_date.weekday() >= 5:
        return {
            "kind": "weekend",
            "label": "周末",
            "data": profile["weekend_style"],
        }
    return {"kind": "weekday", "label": "工作日", "data": {}}


def build_subject(
    rng: random.Random, profile: dict, slot: str, alias: str, context: dict
) -> str:
    slot_name = slot_config(profile, slot)["title"]
    base_subjects = [
        f"{alias}，{slot_name}呀",
        f"给{alias}的{slot_name}小信",
        f"{alias}今天也要被偏爱",
        f"{slot_name}时间到，来抱抱我的{alias}",
    ]
    if context["kind"] == "holiday":
        holiday_name = context["label"]
        base_subjects.extend(
            [
                f"{holiday_name}快乐，{alias}",
                f"{holiday_name}限定问候送给{alias}",
                f"{alias}的{holiday_name}专属偏爱",
            ]
        )
    if context["kind"] == "weekend":
        base_subjects.extend(
            [
                f"周末版{slot_name}，发给{alias}",
                f"{alias}，今天慢一点也没关系",
            ]
        )
    return choose(rng, base_subjects)


def build_lines(
    rng: random.Random, profile: dict, slot: str, alias: str, context: dict
) -> tuple[list[str], str]:
    slot_data = slot_config(profile, slot)
    notes = profile["relationship_notes"]
    tone = profile["voice"]
    signature = choose(rng, profile["signatures"])

    opener = choose(rng, slot_data["openers"]).format(alias=alias)
    mood = choose(rng, slot_data["mood_lines"])
    care = choose(rng, slot_data["care_lines"])
    closer = choose(rng, slot_data["closers"]).format(alias=alias)
    memory = choose(rng, notes["private_feelings"])
    habit = choose(rng, notes["care_habits"])
    sparkle = choose(rng, profile["visual_signs"])

    extra_lines: list[str] = []
    if context["kind"] == "holiday":
        holiday_data = context["data"]
        extra_lines.append(
            f"今天是{context['label']}，{holiday_data.get('mood', '所以我想把特别一点的喜欢先给你。')}"
        )
        holiday_lines = holiday_data.get("extra_lines", [])
        if holiday_lines:
            extra_lines.append(choose(rng, holiday_lines))
    elif context["kind"] == "weekend":
        extra_lines.append(choose(rng, profile["weekend_style"]["extra_lines"]))

    note_candidates = [
        f"我知道你有时候会嘴上说还好，但我还是会下意识想提醒你：{habit}",
        f"说到底，我就是想把这些小关心留给你，像{tone['soft_metaphor']}一样慢慢落在你身上。",
        f"今天也想认真告诉你，{memory}",
        f"如果你这会儿正忙，那我就先把这封小邮件放在这里，等你空下来再拆开我的惦记。",
    ]
    chosen_notes = pick_unique(rng, note_candidates, 2)

    lines = [opener, mood, *extra_lines, *chosen_notes, care, closer, sparkle]
    return lines, signature


def build_plain_and_html(slot: str, send_date: dt.date) -> tuple[str, str, str, str]:
    profile = load_profile()
    rng = build_rng(send_date, slot)
    alias = choose(rng, profile["aliases"])
    context = day_context(profile, send_date)
    subject = build_subject(rng, profile, slot, alias, context)
    lines, signature = build_lines(rng, profile, slot, alias, context)
    slot_title = slot_config(profile, slot)["title"]

    plain = "\n".join(
        [
            f"{slot_title}呀，{alias}：",
            "",
            *lines,
            "",
            signature,
        ]
    )

    line_html = "".join(
        f'<p style="margin:0 0 14px 0;">{escape(line)}</p>' for line in lines[:-1]
    )
    accent = escape(slot_config(profile, slot)["accent"])
    context_badge = escape(context["label"])
    alias_html = escape(alias)
    signature_html = escape(signature)
    sparkle_html = escape(lines[-1])
    title_html = escape(slot_title)

    html = f"""\
<!DOCTYPE html>
<html lang="zh-CN">
  <body style="margin:0;padding:0;background:#fff8fb;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;color:#3f2a35;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#fff8fb;padding:14px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:560px;background:#ffffff;border-radius:26px;overflow:hidden;border:1px solid #ffd9e6;">
            <tr>
              <td style="padding:22px 22px 18px 22px;background:linear-gradient(135deg,#ff8aa8 0%,#ffc9d7 100%);color:#ffffff;">
                <div style="display:inline-block;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,0.22);font-size:13px;letter-spacing:0.5px;">{context_badge} · {accent}</div>
                <div style="margin-top:12px;font-size:30px;font-weight:700;line-height:1.3;">{title_html}，{alias_html}</div>
                <div style="margin-top:8px;font-size:15px;line-height:1.7;opacity:0.96;">这是一封定时送达的小偏爱。</div>
              </td>
            </tr>
            <tr>
              <td style="padding:24px 22px 18px 22px;">
                <div style="font-size:16px;line-height:1.9;color:#4d3340;">
                  {line_html}
                </div>
                <div style="margin-top:10px;padding:14px 16px;border-radius:18px;background:#fff3f8;border:1px dashed #ffbdd0;font-size:14px;line-height:1.8;color:#8d6071;">
                  {sparkle_html}
                </div>
              </td>
            </tr>
            <tr>
              <td style="padding:0 22px 24px 22px;">
                <div style="border-top:1px solid #f5d9e4;padding-top:16px;font-size:15px;line-height:1.8;color:#6f4a59;">
                  <div>♥ ♥ ♥</div>
                  <div style="margin-top:8px;">{signature_html}</div>
                </div>
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""
    return subject, plain, html, context["kind"]


def build_message(to_address: str, subject: str, plain: str, html: str) -> EmailMessage:
    sender = send_email.env_value("AUTO_EMAIL_FROM") or send_email.env_value(
        "AUTO_EMAIL_SMTP_USER"
    )
    if not sender:
        raise SystemExit(
            "Missing sender address. Set AUTO_EMAIL_FROM or AUTO_EMAIL_SMTP_USER."
        )

    message = EmailMessage()
    message["From"] = sender
    message["To"] = to_address
    message["Subject"] = subject
    message.set_content(plain)
    message.add_alternative(html, subtype="html")
    return message


def main() -> None:
    args = parse_args()
    send_date = resolve_date(args.date)
    subject, plain, html, context_kind = build_plain_and_html(args.slot, send_date)
    message = build_message(args.to, subject, plain, html)

    if args.dry_run:
        print("Dry run successful.")
        print(f"Slot: {args.slot}")
        print(f"Date: {send_date.isoformat()}")
        print(f"Context: {context_kind}")
        print(f"To: {args.to}")
        print(f"Subject: {subject}")
        print("HTML body: yes")
        return

    with send_email.connect() as server:
        server.send_message(message, to_addrs=[args.to])

    print("Love greeting sent successfully.")
    print(f"Slot: {args.slot}")
    print(f"Date: {send_date.isoformat()}")
    print(f"Context: {context_kind}")
    print(f"To: {args.to}")
    print(f"Subject: {subject}")


if __name__ == "__main__":
    main()
