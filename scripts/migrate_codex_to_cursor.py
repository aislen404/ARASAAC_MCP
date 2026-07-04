#!/usr/bin/env python3
"""Deprecated: use scripts/sync_agent_packs.py instead."""

from sync_agent_packs import main

if __name__ == "__main__":
    print("Note: migrate_codex_to_cursor.py is deprecated. Running sync_agent_packs.py...")
    main()
