#!/usr/bin/env python3
"""
Weekly planning tool.
Asks about your upcoming week and creates Apple Calendar events.
No API key required.

Run: python3 agent.py
  or double-click run-agent.command
"""

import sys
from datetime import date, timedelta
from calendar_utils import create_calendar_event

DAYS = {"mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6}

DAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

DAY_CALENDARS = [
    ("Social Life",  "dinners, meetups, parties, dates"),
    ("Workout",      "gym, runs, yoga, spin, classes"),
]

REMAINING_CALENDARS = [
    ("Recruitment",  "interviews, coffee chats, recruiter calls"),
    ("Appointments", "medical, dentist, errands, admin"),
]


def week_start() -> date:
    today = date.today()
    days_to_monday = (7 - today.weekday()) % 7 or 7
    return today + timedelta(days=days_to_monday)


def parse_day(s: str, monday: date):
    key = s.strip().lower()[:3]
    if key not in DAYS:
        return None
    return monday + timedelta(days=DAYS[key])


def parse_time(s: str):
    """Accept '7pm', '7:30pm', '9am', '14:00', '9:30' → 'HH:MM'."""
    s = s.strip().lower()
    pm = s.endswith("pm")
    am = s.endswith("am")
    s = s.removesuffix("pm").removesuffix("am").strip()
    try:
        if ":" in s:
            h, m = int(s.split(":")[0]), int(s.split(":")[1])
        else:
            h, m = int(s), 0
    except ValueError:
        return None
    if pm and h != 12:
        h += 12
    if am and h == 12:
        h = 0
    if not (0 <= h <= 23 and 0 <= m <= 59):
        return None
    return f"{h:02d}:{m:02d}"


def add_one_hour(t: str) -> str:
    h, m = int(t[:2]), int(t[3:])
    h = (h + 1) % 24
    return f"{h:02d}:{m:02d}"


def fmt_time(t: str) -> str:
    h, m = int(t[:2]), int(t[3:])
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d} {period}"


def collect_event(calendar: str, event_date: date, prompt: str) -> bool:
    """Prompt for one event on a known date. Returns True if an event was added."""
    title = input(prompt).strip()
    if not title:
        return False

    while True:
        start_str = input("    Start time (e.g. 9am, 2:30pm, 14:00): ").strip()
        start_time = parse_time(start_str)
        if start_time:
            break
        print("    ✗ Try formats like 9am, 7:30pm, or 14:00.")

    while True:
        end_str = input("    End time (Enter = +1 hour): ").strip()
        if not end_str:
            end_time = add_one_hour(start_time)
            break
        end_time = parse_time(end_str)
        if end_time:
            break
        print("    ✗ Try formats like 9am, 7:30pm, or 14:00.")

    try:
        create_calendar_event(
            calendar=calendar,
            title=title,
            date=event_date.isoformat(),
            start_time=start_time,
            end_time=end_time,
        )
        print(f"    ✓ '{title}' → {fmt_time(start_time)}–{fmt_time(end_time)}")
    except Exception as e:
        print(f"    ✗ Couldn't create event: {e}")

    return True


def collect_day(day_name: str, event_date: date) -> None:
    label = f"{day_name} {event_date.strftime('%b %-d')}"
    print(f"\n── {label} {'─' * max(0, 40 - len(label))}")

    for calendar, _ in DAY_CALENDARS:
        first = True
        while True:
            prompt = f"    {calendar} event (or Enter to skip): " if first else f"    Another {calendar} event? (or Enter to skip): "
            first = False
            if not collect_event(calendar, event_date, prompt):
                break


def collect_calendar(calendar: str, description: str, monday: date) -> None:
    print(f"\n── {calendar.upper()}  ({description})")
    while True:
        title = input("  Event name (or Enter to skip): ").strip()
        if not title:
            break

        while True:
            day_str = input("  Day (Mon Tue Wed Thu Fri Sat Sun): ").strip()
            event_date = parse_day(day_str, monday)
            if event_date:
                break
            print("  ✗ Didn't catch that — try Mon, Tue, Wed…")

        while True:
            start_str = input("  Start time (e.g. 9am, 2:30pm, 14:00): ").strip()
            start_time = parse_time(start_str)
            if start_time:
                break
            print("  ✗ Try formats like 9am, 7:30pm, or 14:00.")

        while True:
            end_str = input("  End time (Enter = +1 hour): ").strip()
            if not end_str:
                end_time = add_one_hour(start_time)
                break
            end_time = parse_time(end_str)
            if end_time:
                break
            print("  ✗ Try formats like 9am, 7:30pm, or 14:00.")

        try:
            create_calendar_event(
                calendar=calendar,
                title=title,
                date=event_date.isoformat(),
                start_time=start_time,
                end_time=end_time,
            )
            print(f"  ✓ {title} added")
        except Exception as e:
            print(f"  ✗ Couldn't create event: {e}")


def main() -> None:
    monday = week_start()
    sunday = monday + timedelta(days=6)

    print()
    print("📅  Weekly Planner")
    print(f"    {monday.strftime('%b %-d')} → {sunday.strftime('%b %-d, %Y')}")
    print()
    print("Social Life & Workout: go day by day.")
    print("Recruitment & Appointments: enter date with each event.")

    # Day-by-day for Social Life and Workout
    for i, day_name in enumerate(DAY_NAMES):
        event_date = monday + timedelta(days=i)
        collect_day(day_name, event_date)

    # Calendar-by-calendar for Recruitment and Appointments
    for calendar, description in REMAINING_CALENDARS:
        collect_calendar(calendar, description, monday)

    print("\n✅  All done — check your calendar. See you next week!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSee you next week! 👋\n")
        sys.exit(0)
