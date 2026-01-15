# Houdini Scene Validator (python)
A Python-based scene validation tool for Houdini that identifies and optionally fixes common pipeline issues.

This tool scans a Houdini scene for common technical issues encountered in production,
including naming conventions, missing file paths, frame settings, and unused nodes.

Issues are presented in a PySide UI where artists or TDs can inspect, filter, and
automatically fix supported problems.

## Features

- Scene-wide validation with modular checks
- Severity-based issue reporting (ERROR / WARNING)
- PySide2 UI with:
  - Severity filters
  - Node selection from issue list
  - Fix Selected / Fix All functionality
- Safe auto-fix system with undo support
- Locked HDA awareness (reported but not modified)
- Structured logging for review or debugging

## Implemented Checks

- Default node naming
- Missing or invalid file paths
- Global frame range validation
- FPS validation (supports standard production rates)
- Unused node detection
- Locked HDA detection

## Architecture

- `checks/` — Individual validation modules, each responsible for:
  - Detecting issues
  - Defining fix behavior
- `validator_core.py` — Aggregates and runs all enabled checks
- `ui/` — PySide2-based interface for issue review and fixing
- `run.py` — Entry point for launching the UI from a shelf tool
- `config/` — Default configuration for severities and behavior

## Design Decisions

- Validation logic is separated from the UI to allow reuse and scalability
- Auto-fixes are opt-in and undo-safe
- Locked HDAs are intentionally not modified, matching studio pipeline constraints
- Severity sorting is handled internally for consistent presentation

## Requirements

- Houdini 20.5+
- Python 3.11
- PySide2 (included with Houdini)

