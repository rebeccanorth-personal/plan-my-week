#!/bin/bash
# Source shell profile so ANTHROPIC_API_KEY and other env vars are available
source ~/.zprofile 2>/dev/null
source ~/.zshrc 2>/dev/null

cd /Users/rebeccanorth/DEV/calendar-agent && python3 agent.py
