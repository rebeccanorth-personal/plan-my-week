# Plan My Week

A local macOS tool that helps you plan your week by walking you through your calendar day by day and creating Apple Calendar events with a few keystrokes.

Every Sunday at 9 AM, a notification fires and a Terminal window opens automatically — ready for you to fill in the week ahead.

## How it works

The agent runs as an interactive CLI:

1. **Day by day (Mon → Sun):** Prompts for Social Life and Workout events on each day. Hit Enter to skip any day or category.
2. **Calendar by calendar:** After all days, prompts for Recruitment and Appointments events (you pick the day per event).

Events are created directly in Apple Calendar via AppleScript — no third-party services or APIs required.

## Calendars

Events are created in four Apple Calendars (which must exist before running):

| Calendar | For |
|---|---|
| **Social Life** | Dinners, meetups, parties, dates |
| **Workout** | Gym, runs, yoga, spin, classes |
| **Recruitment** | Interviews, coffee chats, recruiter calls |
| **Appointments** | Medical, dentist, errands, admin |

## Requirements

- macOS (uses AppleScript via `osascript`)
- Python 3.9+
- The four Apple Calendars listed above must exist in your Calendar app

## Setup

### Run manually

```bash
git clone https://github.com/rebeccanorth-personal/plan-my-week.git
cd plan-my-week
python3 agent.py
```

### Automate with launchd (Sunday 9 AM)

The `launchd/` folder contains a LaunchAgent plist that fires every Sunday at 9 AM.

**Before installing**, update the hardcoded paths in these files to match your username/directory:
- `notify-and-launch.sh` — path to `run-agent.command`
- `run-agent.command` — path to the project directory
- `launchd/com.rebeccanorth.calendar-agent.plist` — path to `notify-and-launch.sh`

Then install:

```bash
cp launchd/com.rebeccanorth.calendar-agent.plist ~/Library/LaunchAgents/
launchctl unload ~/Library/LaunchAgents/com.rebeccanorth.calendar-agent.plist 2>/dev/null
launchctl load   ~/Library/LaunchAgents/com.rebeccanorth.calendar-agent.plist
```

Test it immediately:

```bash
launchctl start com.rebeccanorth.calendar-agent
```

## Files

| File | Purpose |
|---|---|
| `agent.py` | Main CLI — day-by-day planning flow |
| `calendar_utils.py` | AppleScript wrapper for creating Calendar events |
| `run-agent.command` | Shell launcher — sources your shell profile and runs the agent |
| `notify-and-launch.sh` | Called by launchd — shows a notification and opens the agent |
| `launchd/com.rebeccanorth.calendar-agent.plist` | LaunchAgent — triggers every Sunday at 9 AM |

## Time input formats

The agent accepts flexible time formats:

```
9am   →  09:00
7pm   →  19:00
2:30pm  →  14:30
14:00   →  14:00
```

End time defaults to +1 hour if you press Enter.
