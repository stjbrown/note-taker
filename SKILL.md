---
name: Note Taker
description: A skill for creating, determining location of, and archiving notes using structured templates.
---

# Note Taker Skill

This skill helps you manage notes within a specific directory structure. It handles daily logs, identifying context from your current work.

## Configuration

The default notes directory is `~/notes`.
You can override this by setting the `NOTES_DIR` environment variable.
Alternatively, you can place a `.env` file in your `NOTES_DIR` with these variables.

### Multi-Agent Configuration
- **AGENT_ID**: Optional. A unique identifier for the current agent/machine (e.g., `work-laptop`, `personal-mac`). If set, daily notes will be suffixed with this ID to prevent conflicts (e.g., `2024-01-25-work-laptop.md`).
- **GIT_SYNC**: Optional. Set to `true` to enable automatic git synchronization (pull before read, push after write).
- **GIT_REPO_URL**: Optional. If set and `NOTES_DIR` is missing, the skill will auto-clone this repo.

## Capabilities

### 1. Create a Daily Note
**When to use**: When the user asks to "take a note", "log this", or record information.
**Template**: `resources/templates/daily.md`
**Naming Convention**: 
- Default: `YYYY-MM-DD.md`
- With `AGENT_ID`: `YYYY-MM-DD-{AGENT_ID}.md`
**Location**: Root of your notes directory.

**Instructions**:
1. Determine the **Context Name**:
    - Check the **Current Working Directory (CWD)**.
    - If the user is in a specific project folder (e.g. `~/code/my-app`), use the folder name (`my-app`) as the **Context Name**.
    - If the user is in a generic location or no distinct project is obvious, use "General" or "Daily Log".
    - *Tip*: If the user explicitly mentions a project ("Take a note for the X project"), use that instead.
2. Run the note creation script:
    ```bash
    python3 scripts/daily_note.py "{Note Content}" --context "{Context Name}"
    ```
    *Note: This script automatically handles loading configuration, git syncing (if enabled), and formatting.*

### 2. Archive Old Notes
**When to use**: To clean up the root directory by moving old daily notes to an archive folder.
**Script**: `scripts/archive_notes.py`

**Usage**:
```bash
python3 /path/to/skill/scripts/archive_notes.py --days 30 --dir /path/to/notes
```
- `--days`: archive notes older than this many days (default: 30).
- `--dir`: the root of your notes directory.

### 4. Research and Note
**When to use**: When the user asks to research a topic and add the findings to their daily notes.

**Instructions**:
1. Identify the topic.
2. Research using `search_web`.
3. Summarize findings.
3. Summarize findings.
4. Run the note creation script:
    ```bash
    python3 scripts/daily_note.py "{Summary of findings}" --context "{Topic}"
    ```

## Future Capabilities
- **Audio to Text**: Transcribe audio using Whisper.

