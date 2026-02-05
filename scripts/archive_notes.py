import os
import shutil
import argparse
from datetime import datetime, timedelta

def archive_notes(notes_dir, days):
    """
    Moves markdown files from the root of notes_dir to an 'archive' subdirectory
    if they are daily notes (YYYY-MM-DD.md) and older than 'days' old.
    """
    archive_dir = os.path.join(notes_dir, "archive")
    if not os.path.exists(archive_dir):
        os.makedirs(archive_dir)
        print(f"Created archive directory: {archive_dir}")

    cutoff_date = datetime.now() - timedelta(days=days)
    count = 0

    for filename in os.listdir(notes_dir):
        file_path = os.path.join(notes_dir, filename)
        
        # Skip directories
        if os.path.isdir(file_path):
            continue
            
        if filename.endswith(".md"):
            # Check for YYYY-MM-DD at the start of the filename
            # This covers "YYYY-MM-DD.md" and "YYYY-MM-DD-agent.md"
            import re
            match = re.match(r"^(\d{4}-\d{2}-\d{2})", filename)
            
            if match:
                try:
                    date_str = match.group(1)
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")
                    
                    if file_date < cutoff_date:
                        shutil.move(file_path, os.path.join(archive_dir, filename))
                        print(f"Archived: {filename}")
                        count += 1
                except ValueError:
                    continue

    print(f"Archiving complete. {count} files moved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Archive old daily notes.")
    parser.add_argument("--dir", required=True, help="The notes directory to clean up")
    parser.add_argument("--days", type=int, default=30, help="Archive notes older than these many days")
    
    args = parser.parse_args()
    
    if not os.path.isdir(args.dir):
        print(f"Error: Directory not found: {args.dir}")
        exit(1)
        
    archive_notes(args.dir, args.days)
