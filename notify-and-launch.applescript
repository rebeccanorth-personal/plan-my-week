-- Shows a notification banner and opens the weekly planning agent in Terminal.
-- Run by launchd every Sunday at 9:00 AM.

display notification "Time to plan your week!" with title "📅 Weekly Planner" sound name "default"

tell application "Terminal"
    activate
    do script "cd /Users/rebeccanorth/DEV/calendar-agent && python3 agent.py"
end tell
