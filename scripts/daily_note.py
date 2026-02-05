import os
import sys
import argparse
import subprocess
from datetime import datetime

def load_env(skill_dir):
    """Load .env file from skill directory if it exists."""
    env_path = os.path.join(skill_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = value

def run_git_command(command, cwd):
    """Run a git command in the specified directory."""
    try:
        subprocess.check_call(command, cwd=cwd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Add a note to the daily log.")
    parser.add_argument("note", help="The content of the note to add.")
    parser.add_argument("--context", default="General", help="The context/heading for the note.")
    args = parser.parse_args()

    # Determine paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    template_path = os.path.join(skill_dir, "resources", "templates", "daily.md")
    
    # Load configuration
    load_env(skill_dir)
    
    notes_dir = os.path.expanduser(os.environ.get("NOTES_DIR", "~/notes"))
    agent_id = os.environ.get("AGENT_ID")
    git_sync = os.environ.get("GIT_SYNC", "false").lower() == "true"
    
    # Ensure notes directory exists
    if not os.path.exists(notes_dir):
        print(f"Error: Notes directory {notes_dir} does not exist.")
        sys.exit(1)

    # Git Sync: Pull
    if git_sync:
        print("Syncing notes (git pull)...")
        if not run_git_command("git pull", notes_dir):
            print("Warning: git pull failed. Proceeding locally.")

    # Determine filename
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{agent_id}.md" if agent_id else f"{today}.md"
    file_path = os.path.join(notes_dir, filename)

    # Prepare note content
    new_note_line = f"- {args.note}\n"
    
    # Read existing content
    content = []
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.readlines()
    else:
        # Create new file from template
        if os.path.exists(template_path):
            with open(template_path, "r") as f:
                template_content = f.read()
                content = template_content.replace("{{ date }}", today).splitlines(keepends=True)
        else:
            content = [f"# Daily Log: {today}\n\n"]

    # Insert note under correct heading
    heading = f"## {args.context}"
    heading_found = False
    insertion_index = -1

    for i, line in enumerate(content):
        if line.strip() == heading:
            heading_found = True
            # Find the end of this section (next heading)
            for j in range(i + 1, len(content)):
                if content[j].startswith("## "):
                    insertion_index = j
                    break
            else:
                insertion_index = len(content)
            break
    
    if heading_found:
        content.insert(insertion_index, new_note_line)
    else:
        # Append new heading and note
        if content and content[-1].strip() != "":
            content.append("\n")
        content.append(f"{heading}\n")
        content.append(new_note_line)

    # Write back to file
    with open(file_path, "w") as f:
        f.writelines(content)
    
    print(f"Note added to {filename} under '{args.context}'.")

    # Git Sync: Push
    if git_sync:
        print("Syncing notes (git push)...")
        run_git_command("git add .", notes_dir)
        run_git_command(f'git commit -m "Auto-save from {agent_id or "skill"}"', notes_dir)
        if run_git_command("git push", notes_dir):
            print("Sync successful.")
        else:
            print("Warning: git push failed.")

if __name__ == "__main__":
    main()
