# Project Overview

## What it does

**Plan My Week** is a personal automation tool for macOS that turns weekly calendar planning into a fast, structured ritual. Every Sunday at 9 AM, a notification fires and a Terminal window opens automatically — ready to walk through the week ahead in under a few minutes.

The agent prompts for events across four life categories:

- **Social Life** — dinners, meetups, parties, dates
- **Workout** — gym, runs, yoga, spin, classes
- **Recruitment** — interviews, coffee chats, recruiter calls
- **Appointments** — medical, dentist, errands, admin

Each input creates a real Apple Calendar event directly — no app-switching, no clicking, no typing into a GUI.

---

## Design decisions

### Why a CLI, not a GUI?

Typing is faster than clicking. A day-by-day prompt forces you to think about each day in sequence, which is actually the right mental model for planning a week. The terminal aesthetic also means there are zero dependencies on frontend frameworks.

### Why AppleScript?

Apple Calendar has no public REST API, but it has a mature AppleScript interface that is fully capable of creating, reading, and deleting events. Using `osascript` to drive AppleScript from Python keeps everything local and offline — no OAuth, no tokens, no sync issues.

The key technical challenge was date arithmetic in AppleScript: setting a month before setting the day can silently overflow (e.g. January 31 → set month to February → February 31 doesn't exist). The fix is to always set `day to 1` before setting the month, then set the final day value after.

### Why launchd, not cron?

On macOS, `launchd` is the native job scheduler and handles sleep/wake cycles correctly — a cron job can miss its window if the machine is asleep at fire time. The `StartCalendarInterval` key in the plist handles this gracefully.

### Why no LLM?

An earlier version explored using the Claude API to interpret free-form input (e.g. "coffee with Sam on Thursday at 3"). In practice, a structured prompt flow was faster and more reliable — the user knows their own events, so the value wasn't in parsing natural language but in making the data-entry loop frictionless.

---

## Architecture

```
agent.py              ← CLI entry point; drives the planning flow
calendar_utils.py     ← AppleScript wrapper; owns all Calendar interaction
run-agent.command     ← Shell launcher; sources env, runs agent.py
notify-and-launch.sh  ← Fired by launchd; shows notification, opens launcher
launchd/              ← LaunchAgent plist; schedules Sunday 9 AM trigger
```

The separation between `agent.py` (flow) and `calendar_utils.py` (Calendar I/O) means the AppleScript layer can be tested or swapped independently of the UI logic.

---

## Stack

| Layer | Technology |
|---|---|
| Language | Python 3.9 |
| Calendar integration | AppleScript via `osascript` |
| Scheduling | macOS launchd |
| Notifications | macOS native (`osascript display notification`) |
| Dependencies | None (stdlib only) |
