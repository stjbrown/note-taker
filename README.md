# Note Taker Skill

A skill for managing structured notes across multiple devices and agents.

## Features
- **Daily Notes**: Automatically creates or appends to daily logs.
- **Context Aware**: Automatically categorizes notes based on your current project/directory.
- **Multi-Agent Sync**: Supports multiple agents writing to the same repository without conflicts.
- **Auto-Archiving**: Scripts to keep your notes folder clean.


## Requirements
- **Python 3.x**: Required for the archiving scripts.
- **Git**: Required for version control and multi-agent synchronization.

## Installation
This skill is designed to be easily added to your AI agent's toolkit.

### 1. Antigravity & General Setup
Clone this repository into your agent's skills directory:
```bash
mkdir -p ~/.agent/skills
cd ~/.agent/skills
git clone <repo_url> note-taker
```

### 2. Cursor, ClaudeCode, Cline, OpenClaw
These agents typically read context from the file system or your current project.
1. **Clone** the repository as shown above (or to any accessible location).
2. **Context Awareness**:
   - **Cursor**: Reference the `SKILL.md` file in your chat (e.g., `@SKILL.md`) to give the agent instructions on how to use this skill.
   - **Cline / OpenClaw**: Ensure the `~/.agent/skills/note-taker/` directory is within the agent's allowed workspace or paths. You may need to ask the agent to "read the note-taker skill instructions" explicitly at the start of a session if it's not automatically loaded.

## Setup

### 1. Environment Variables
Configure the following environment variables in your agent's profile. **Alternatively**, you can create a `.env` file in your `NOTES_DIR` (see `resources/.env.example`).

| Variable | Description | Default |
|----------|-------------|---------|
| `NOTES_DIR` | Path to your notes directory. | `~/notes` |
| `AGENT_ID` | **Required for Multi-Agent**. Unique ID for this machine/agent (e.g., `work`, `home`). | `None` |
| `GIT_SYNC` | Set to `true` to enable auto-commit and push/pull. | `false` |
| `GIT_REPO_URL` | Optional. URL to clone if `NOTES_DIR` is missing. | `None` |

#### Using a .env file
Create a file named `.env` in the **Skill Directory** (e.g., `~/.agent/skills/note-taker/`). This ensures configuration is loaded even if the notes directory doesn't exist yet.
```bash
NOTES_DIR=~/notes
AGENT_ID=work-laptop
GIT_SYNC=true
GIT_REPO_URL=https://github.com/user/notes.git
```

### Configuration Precedence
If variables are defined in multiple places, this order is used (highest to lowest):
1. **System Environment Variables** (`export AGENT_ID=...`)
2. **Skill Directory `.env`** (`~/.agent/skills/note-taker/.env`)
3. **Notes Directory `.env`** (`~/notes/.env`)

### 2. Multi-Agent Git Setup
To use this skill across multiple machines:

1. **Initialize Git Repository**:
   ```bash
   mkdir ~/notes
   cd ~/notes
   git init
   git remote add origin <your-repo-url>
   ```

2. **Configure Each Agent**:
   - **Machine A (Work)**:
     ```bash
     export NOTES_DIR=~/notes
     export AGENT_ID=work
     export GIT_SYNC=true
     ```
   - **Machine B (Personal)**:
     ```bash
     export NOTES_DIR=~/notes
     export AGENT_ID=personal
     export GIT_SYNC=true
     ```

## Usage

### Context Aware Notes
The skill checks your **Current Working Directory**.
- If you are in `~/code/my-app`, the note will be added under the `## my-app` heading in today's daily note.
- If you are in a generic location, it defaults to `## General`.

**Example**:
> "Take a note to check the build script"
(If in `~/code/backend`) -> Appends to `2024-02-05-work.md` under `## backend`.

### Archiving
To archive old notes (older than 30 days):
```bash
python3 scripts/archive_notes.py --dir ~/notes --days 30
```
*Note: This script handles both standard `YYYY-MM-DD.md` and fragmented `YYYY-MM-DD-{AGENT_ID}.md` files.*
