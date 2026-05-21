#!/bin/bash
# Called by terminal-notifier when you click the Sunday notification.
# Opens a new Terminal window and starts the weekly planning agent.
osascript \
  -e 'tell application "Terminal" to activate' \
  -e 'tell application "Terminal" to do script "cd /Users/rebeccanorth/DEV/calendar-agent && python3 agent.py"'
