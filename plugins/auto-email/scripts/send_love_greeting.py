#!/usr/bin/env python3
"""Generate and send a profile-driven love email with surprise cadence."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import random
import sys
from dataclasses import dataclass
from email.message import EmailMessage
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

import send_email


PROFILE_PATH = (
    Path(__file__).resolve().parent.parent / "data" / "love_greeting_profile.json"
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

DEFAULT_HOLIDAYS = {
    "01-01": {"name": "元旦", "tone": "新年", "mood": "新一年的偏爱也先给你。"},
    "02-14": {"name": "情人节", "tone": "浪漫", "mood": "今天适合明目张胆地多喜欢你一点。"},
    "03-08": {"name": "女神节", "tone": "宠溺", "mood": "今天就请你负责漂亮和开心。"},
    "05-20": {"name": "520", "tone": "表白", "mood": "这种日子就该认真说一句，我真的很喜欢你。"},
    "06-01": {"name": "儿童节", "tone": "俏皮", "mood": "今天允许你当一天被宠着的小朋友。"},
    "10-01": {"name": "国庆节", "tone": "假期", "mood": "假期也要被我惦记着，轻轻松松去开心。"},
    "12-24": {"name": "平安夜", "tone": "温柔", "mood": "今晚想把平安和偏爱一起装进这封信里。"},
    "12-25": {"name": "圣诞节", "tone": "礼物感", "mood": "今天的你像被节日特地偏爱了一下。"},
}


@dataclass
class SendDecision:
    should_send: bool
    reason: str
    context_kind: str
    holiday_name: str | None = None
    target_slot: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send a profile-driven love email.")
    parser.add_argument("--to", required=True, help="Recipient address")
    parser.add_argument("--date", help="Override local date in YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force-send", action="store_true")
    return parser.parse_args()


def current_timezone() -> ZoneInfo:
    timezone_name = send_email.env_value("AUTO_EMAIL_TIMEZONE") or "Asia/Shanghai"
    try:
        return ZoneInfo(timezone_name)
    except Exception as exc:
        raise SystemExit(f"Invalid AUTO_EMAIL_TIMEZONE value: {timezone_name}") from exc


def resolve_now(date_text: str | None) -> dt.datetime:
    tz = current_timezone()
    if date_text:
        return dt.datetime.combine(dt.date.fromisoformat(date_text), dt.time(20, 17), tz)
    return dt.datetime.now(tz)


def load_profile() -> dict:
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def build_rng(seed: str) -> random.Random:
    return random.Random(seed)


def choose(rng: random.Random, values: list[str]) -> str:
    return values[rng.randrange(len(values))]


def choose_unique(rng: random.Random, values: list[str], count: int) -> list[str]:
    if len(values) <= count:
        return list(values)
    return rng.sample(values, count)


def find_holiday(profile: dict, send_date: dt.date) -> dict | None:
    date_key = send_date.strftime("%m-%d")
    custom = profile.get("special_dates", {})
    if date_key in custom:
        payload = dict(custom[date_key])
        payload.setdefault("name", date_key)
        return payload
    if date_key in DEFAULT_HOLIDAYS:
        return dict(DEFAULT_HOLIDAYS[date_key])
    return None


def evaluate_send_decision(profile: dict, send_dt: dt.datetime, force_send: bool) -> SendDecision:
    target_hour, target_minute = daily_target_slot(profile, send_dt.date())
    target_slot = f"{target_hour:02d}:{target_minute:02d}"

    if force_send:
        return SendDecision(True, "manual override", "manual", target_slot=target_slot)

    current_slot = (send_dt.hour, send_dt.minute)
    if current_slot != (target_hour, target_minute):
        return SendDecision(False, f"waiting for daily slot {target_slot}", "skip", target_slot=target_slot)

    send_date = send_dt.date()
    holiday = find_holiday(profile, send_date)
    if holiday is not None:
        return SendDecision(True, "holiday rule", "holiday", holiday["name"], target_slot)

    if send_date.weekday() >= 5:
        return SendDecision(True, "weekend daily rule", "weekend", target_slot=target_slot)

    return SendDecision(True, "weekday daily rule", "weekday", target_slot=target_slot)


def daily_target_slot(profile: dict, send_date: dt.date) -> tuple[int, int]:
    schedule = profile["schedule"]
    start_hour = int(schedule["awake_start_hour"])
    end_hour = int(schedule["awake_end_hour"])
    check_minutes = [int(value) for value in schedule["check_minutes"]]
    slots = [(hour, minute) for hour in range(start_hour, end_hour + 1) for minute in check_minutes]
    rng = build_rng(f"{send_date.isoformat()}:daily-time-slot")
    return choose(rng, slots)


def relationship_counter(profile: dict, send_dt: dt.datetime) -> dict[str, int]:
    meet_dt = dt.datetime.fromisoformat(profile["relationship"]["met_on_datetime"]).replace(
        tzinfo=current_timezone()
    )
    delta = send_dt - meet_dt
    total_seconds = max(int(delta.total_seconds()), 0)
    days = total_seconds // 86400
    hours = total_seconds // 3600
    minutes = total_seconds // 60
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": total_seconds,
    }


def theme_pack(profile: dict, rng: random.Random) -> dict:
    return choose(rng, profile["ui_themes"])


def build_subject(
    rng: random.Random,
    profile: dict,
    recipient_alias: str,
    decision: SendDecision,
) -> str:
    base = [
        f"{recipient_alias}，今天这封信是给你的",
        f"给{recipient_alias}的小惊喜",
        f"{recipient_alias}，来拆一下我今天的偏爱",
        f"今天也想悄悄偏心一下{recipient_alias}",
    ]
    if decision.context_kind == "holiday" and decision.holiday_name:
        base.extend(
            [
                f"{decision.holiday_name}快乐，{recipient_alias}",
                f"{recipient_alias}的{decision.holiday_name}限定来信",
            ]
        )
    if decision.context_kind == "weekend":
        base.extend(
            [
                f"周末给{recipient_alias}的轻松来信",
                f"{recipient_alias}，今天慢一点也可以",
            ]
        )
    if decision.context_kind == "surprise":
        base.extend(
            [
                f"{recipient_alias}，今天是惊喜空投",
                f"没有理由，就是想给{recipient_alias}写信",
            ]
        )
    return choose(rng, base)


def build_body(
    profile: dict,
    send_dt: dt.datetime,
    decision: SendDecision,
) -> tuple[str, str, dict]:
    send_date = send_dt.date()
    rng = build_rng(f"{send_date.isoformat()}:{decision.context_kind}")
    relationship = profile["relationship"]
    recipient_alias = choose(rng, profile["recipient_aliases"])
    sender_name = choose(rng, profile["sender_names"])
    signature = choose(rng, profile["signatures"])
    theme = theme_pack(profile, rng)
    counter = relationship_counter(profile, send_dt)
    show_counter = (
        decision.context_kind == "holiday"
        or build_rng(f"{send_date.isoformat()}:counter").random()
        < float(profile["ui_modules"]["counter_probability"])
    )
    show_memory = (
        decision.context_kind in {"holiday", "surprise", "weekend"}
        or build_rng(f"{send_date.isoformat()}:memory").random()
        < float(profile["ui_modules"]["memory_probability"])
    )

    opener = choose(rng, profile["voice_blocks"]["openers"]).format(alias=recipient_alias)
    care = choose(rng, profile["voice_blocks"]["care"]).format(alias=recipient_alias)
    warmth = choose(rng, profile["voice_blocks"]["warmth"])
    closer = choose(rng, profile["voice_blocks"]["closers"]).format(alias=recipient_alias)
    visual_sign = choose(rng, profile["visual_signs"])
    memory = choose(rng, profile["memory_fragments"]) if show_memory else None
    micro_line = choose(rng, profile["micro_lines"])

    special_line = None
    if decision.context_kind == "holiday":
        holiday = find_holiday(profile, send_date)
        if holiday:
            special_line = f"今天是{holiday['name']}，{holiday['mood']}"
    elif decision.context_kind == "weekend":
        special_line = choose(rng, profile["weekend_lines"])
    elif decision.context_kind == "surprise":
        special_line = choose(rng, profile["surprise_lines"])

    sender_badge = f"{sender_name} · {relationship['english_sender_alias']}"
    chip_text = choose(rng, profile["decorative_chips"])

    plain_lines = [
        f"{recipient_alias}：",
        "",
        opener,
        warmth,
    ]
    if special_line:
        plain_lines.append(special_line)
    if memory:
        plain_lines.append(f"今天突然想起：{memory}")
    plain_lines.extend([care, closer, visual_sign, "", signature])
    plain = "\n".join(plain_lines)

    sections: list[str] = [
        f'<p style="margin:0 0 14px 0;">{escape(opener)}</p>',
        f'<p style="margin:0 0 14px 0;">{escape(warmth)}</p>',
    ]
    if special_line:
        sections.append(
            '<div style="margin:0 0 16px 0;padding:12px 14px;border-radius:16px;'
            f'background:{theme["soft"]};border:1px solid {theme["border"]};font-size:14px;'
            f'line-height:1.8;color:{theme["muted"]};">{escape(special_line)}</div>'
        )
    if memory:
        sections.append(
            '<div style="margin:0 0 16px 0;padding:14px 16px;border-radius:18px;'
            f'background:{theme["memory_bg"]};border:1px dashed {theme["memory_border"]};'
            f'font-size:15px;line-height:1.85;color:{theme["text"]};">'
            f'<div style="font-size:12px;letter-spacing:0.5px;text-transform:uppercase;opacity:0.7;">'
            'Memory Flashback</div>'
            f'<div style="margin-top:8px;">{escape(memory)}</div>'
            "</div>"
        )
    sections.append(f'<p style="margin:0 0 14px 0;">{escape(care)}</p>')
    sections.append(f'<p style="margin:0;">{escape(closer)}</p>')

    counter_html = ""
    if show_counter:
        counter_html = (
            '<div style="margin:18px 0 0 0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));'
            'gap:10px;">'
            + "".join(
                [
                    stat_card("认识天数", f"{counter['days']} 天", theme),
                    stat_card("一起走过", f"{counter['hours']} 小时", theme),
                    stat_card("细细算算", f"{counter['minutes']} 分钟", theme),
                    stat_card("偷偷偏爱", f"{counter['seconds']} 秒", theme),
                ]
            )
            + "</div>"
        )

    html = f"""\
<!DOCTYPE html>
<html lang="zh-CN">
  <body style="margin:0;padding:0;background:{theme['page']};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;color:{theme['text']};">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{theme['page']};padding:18px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:620px;background:{theme['card']};border-radius:28px;overflow:hidden;border:1px solid {theme['border']};box-shadow:{theme['shadow']};">
            <tr>
              <td style="padding:26px 24px 20px 24px;background:{theme['hero']};color:#ffffff;">
                <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;">
                  <div>
                    <div style="display:inline-block;padding:6px 12px;border-radius:999px;background:rgba(255,255,255,0.18);font-size:12px;letter-spacing:0.6px;">{escape(chip_text)}</div>
                    <div style="margin-top:14px;font-size:31px;line-height:1.28;font-weight:700;">{escape(recipient_alias)}</div>
                    <div style="margin-top:8px;font-size:15px;line-height:1.8;opacity:0.95;">{escape(micro_line)}</div>
                  </div>
                  <div style="min-width:120px;text-align:right;font-size:12px;line-height:1.8;opacity:0.92;">
                    <div>{escape(sender_badge)}</div>
                    <div>{escape(decision.reason)}</div>
                  </div>
                </div>
              </td>
            </tr>
            <tr>
              <td style="padding:24px;">
                <div style="font-size:16px;line-height:1.95;color:{theme['text']};">
                  {''.join(sections)}
                </div>
                {counter_html}
              </td>
            </tr>
            <tr>
              <td style="padding:0 24px 24px 24px;">
                <div style="padding:16px 18px;border-radius:20px;background:{theme['footer_bg']};border:1px solid {theme['border']};">
                  <div style="font-size:14px;line-height:1.9;color:{theme['muted']};">{escape(visual_sign)}</div>
                  <div style="margin-top:10px;font-size:15px;line-height:1.8;color:{theme['text']};">—— {escape(signature)}</div>
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
    meta = {
        "recipient_alias": recipient_alias,
        "sender_name": sender_name,
        "signature": signature,
        "theme_name": theme["name"],
        "show_counter": show_counter,
        "context_kind": decision.context_kind,
    }
    subject = build_subject(rng, profile, recipient_alias, decision)
    return subject, plain, html, meta


def stat_card(label: str, value: str, theme: dict) -> str:
    return (
        f'<div style="padding:14px 14px 12px 14px;border-radius:18px;background:{theme["soft"]};'
        f'border:1px solid {theme["border"]};">'
        f'<div style="font-size:12px;line-height:1.6;color:{theme["muted"]};">{escape(label)}</div>'
        f'<div style="margin-top:4px;font-size:18px;font-weight:700;color:{theme["text"]};">{escape(value)}</div>'
        "</div>"
    )


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
    send_dt = resolve_now(args.date)
    profile = load_profile()
    decision = evaluate_send_decision(profile, send_dt, args.force_send)

    if not decision.should_send:
        print("Skipped love greeting.")
        print(f"Date: {send_dt.date().isoformat()}")
        print(f"Reason: {decision.reason}")
        if decision.target_slot:
            print(f"Target slot: {decision.target_slot}")
        return

    subject, plain, html, meta = build_body(profile, send_dt, decision)
    message = build_message(args.to, subject, plain, html)

    if args.dry_run:
        print("Dry run successful.")
        print(f"Date: {send_dt.date().isoformat()}")
        print(f"Reason: {decision.reason}")
        print(f"Context: {decision.context_kind}")
        print(f"Target slot: {decision.target_slot}")
        print(f"Theme: {meta['theme_name']}")
        print(f"Counter module: {'yes' if meta['show_counter'] else 'no'}")
        print(f"To: {args.to}")
        print(f"Subject: {subject}")
        return

    with send_email.connect() as server:
        server.send_message(message, to_addrs=[args.to])

    print("Love greeting sent successfully.")
    print(f"Date: {send_dt.date().isoformat()}")
    print(f"Reason: {decision.reason}")
    print(f"Context: {decision.context_kind}")
    print(f"Target slot: {decision.target_slot}")
    print(f"Theme: {meta['theme_name']}")
    print(f"To: {args.to}")
    print(f"Subject: {subject}")


if __name__ == "__main__":
    main()
