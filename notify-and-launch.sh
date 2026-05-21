#!/bin/bash
# Fired by launchd every Sunday at 9:00 AM.

/usr/bin/osascript -e 'display notification "Time to plan your week!" with title "📅 Weekly Planner" sound name "default"'

open /Users/rebeccanorth/DEV/calendar-agent/run-agent.command
