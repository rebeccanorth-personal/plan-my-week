"""
Apple Calendar integration via osascript.
"""

import subprocess
from datetime import datetime

CALENDARS = ["Social Life", "Workout", "Recruitment", "Appointments"]


def create_calendar_event(
    calendar: str,
    title: str,
    date: str,
    start_time: str,
    end_time: str,
    notes: str = "",
) -> str:
    """Create an event in Apple Calendar. Returns a confirmation string."""
    if calendar not in CALENDARS:
        raise ValueError(f"Unknown calendar '{calendar}'. Must be one of: {CALENDARS}")

    start_dt = datetime.strptime(f"{date} {start_time}", "%Y-%m-%d %H:%M")
    end_dt = datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M")

    start_secs = start_dt.hour * 3600 + start_dt.minute * 60
    end_secs = end_dt.hour * 3600 + end_dt.minute * 60

    # Escape for AppleScript string literals
    def esc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"')

    # Build event properties (conditionally include description)
    props_parts = [f'summary:"{esc(title)}"', "start date:sd", "end date:ed"]
    if notes:
        props_parts.append(f'description:"{esc(notes)}"')
    props_str = ", ".join(props_parts)

    # Set day to 1 first to avoid month-overflow errors (e.g. Jan 31 → April)
    script = f"""
tell application "Calendar"
    tell calendar "{esc(calendar)}"
        set sd to current date
        set year of sd to {start_dt.year}
        set day of sd to 1
        set month of sd to {start_dt.month}
        set day of sd to {start_dt.day}
        set time of sd to {start_secs}

        set ed to current date
        set year of ed to {end_dt.year}
        set day of ed to 1
        set month of ed to {end_dt.month}
        set day of ed to {end_dt.day}
        set time of ed to {end_secs}

        make new event with properties {{{props_str}}}
    end tell
end tell
"""

    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=10,
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "osascript failed with no output")

    start_disp = start_dt.strftime("%-I:%M %p")
    end_disp = end_dt.strftime("%-I:%M %p")
    date_disp = start_dt.strftime("%a %b %-d")
    return f"'{title}' → {calendar}  |  {date_disp}  {start_disp}–{end_disp}"
