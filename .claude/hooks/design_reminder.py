"""PostToolUse hook: remind Claude of the design rules after editing site files.

Fires once per session per file, so a run of edits to one file is not noisy.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

WATCHED = ("data/", "templates/", "pipeline/", "docs/", ".github/", "README.md")
SKIP = ("data/cache/", "data/news/drafts/")


def main() -> None:
    payload = json.load(sys.stdin)
    path = payload.get("tool_input", {}).get("file_path") or ""
    root = os.environ.get("CLAUDE_PROJECT_DIR", payload.get("cwd", ""))
    try:
        rel = Path(path).resolve().relative_to(Path(root).resolve()).as_posix()
    except ValueError:
        return
    if not rel.startswith(WATCHED) or rel.startswith(SKIP):
        return

    seen = Path(tempfile.gettempdir()) / f"website-design-{payload.get('session_id', 'x')}"
    done = seen.read_text().splitlines() if seen.exists() else []
    if rel in done:
        return
    seen.write_text("\n".join([*done, rel]))

    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PostToolUse",
        "additionalContext": (
            f"Design check ({rel}): prose follows design-prose (W1-W8). If this edit breaks "
            "a rule, flag **Design warning**. If it sets or changes a pattern, write "
            "**Design change proposed** in chat and wait for approval. Never edit the "
            "skills, hooks or CLAUDE.md unapproved."
        ),
    }}))


if __name__ == "__main__":
    main()
