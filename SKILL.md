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
1. **Load Configuration**:
    - Resolve configuration values using the following **Priority Order** (highest to lowest):
        1. **System Environment Variables**: (e.g. `export AGENT_ID=foo`)
        2. **Skill Directory `.env`**: (`~/.agent/skills/note-taker/.env`)
        3. **Notes Directory `.env`**: (`$NOTES_DIR/.env`)
    - *Note*: Higher priority sources override lower ones.
    - **Auto-Clone**: If `NOTES_DIR` does NOT exist and `GIT_REPO_URL` is resolved:
        - Run `git clone {GIT_REPO_URL} {NOTES_DIR}`.
    - **Initialization**:
        - Check if `NOTES_DIR` exists.
        - Check if `.gitignore` exists in `NOTES_DIR`.
        - If missing, create it with content: `.env`.
        - If present, ensure `.env` is listed within it.
2. **Git Sync (Start)**: If `GIT_SYNC` is `true`, run `git pull` in the notes directory.
3. **Context Detection**:
    - Check the **Current Working Directory (CWD)**.
    - If the user is in a specific project folder (e.g. `~/code/my-app`), use the folder name (`my-app`) as the **Context Name**.
    - If the user is in a generic location (home dir, Desktop) or no distinct project is obvious, use "General" or "Daily Log" as the Context Name.
    - *Tip*: If the user explicitly mentions a project ("Take a note for the X project"), use that instead.
3. Determine the filename:
    - Get current date `YYYY-MM-DD`.
    - Check for `AGENT_ID` env var.
    - If set, filename is `YYYY-MM-DD-{AGENT_ID}.md`.
    - Else, filename is `YYYY-MM-DD.md`.
4. Check if the file exists in the notes directory.
5. If it does not exist:
    - Copy the content of `resources/templates/daily.md` to the new file and fill in the date.
6. If it exists (or after creation):
    - Read the current file content.
    - Check if a Heading matching the **Context Name** exists (e.g. `## my-app`).
    - If the heading exists:
        - Append the new note as a bullet point under that heading.
    - If the heading does not exist:
        - Add the new heading (`## {Context Name}`) to the end of the file and add the note as a bullet point under it.
7. **Git Sync (End)**: If `GIT_SYNC` is `true`:
    - Run `git add .`
    - Run `git commit -m "Auto-save from {AGENT_ID or 'default'}"`
    - Run `git push`

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
4. Follow "Create a Daily Note" instructions to add the summary.

## Future Capabilities
- **Audio to Text**: Transcribe audio using Whisper.

