#!/usr/bin/env bash
# Copies the team into a project.
# Usage: ./install.sh /path/to/project            (generic team)
#        ./install.sh /path/to/project nutritale  (a saved project team)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:?Give the path to your project}"
PROFILE="${2:-}"
[ -d "$TARGET" ] || { echo "Not a folder: $TARGET"; exit 1; }
mkdir -p "$TARGET/.claude/agents" "$TARGET/.claude/skills"
copy() { # never overwrite a file that is already there
  if [ -e "$2" ]; then echo "kept (already exists): $2"; else cp -r "$1" "$2"; echo "added: $2"; fi
}
if [ -n "$PROFILE" ]; then
  P="$HERE/projects/$PROFILE"; [ -d "$P" ] || { echo "No such project team: $PROFILE"; exit 1; }
  for f in "$P"/agents/*.md; do copy "$f" "$TARGET/.claude/agents/$(basename "$f")"; done
  copy "$P/CLAUDE.md" "$TARGET/CLAUDE.md"
  copy "$P/AGENT_JOBS.md" "$TARGET/.claude/AGENT_JOBS.md"
else
  for f in "$HERE"/agents/*.md; do copy "$f" "$TARGET/.claude/agents/$(basename "$f")"; done
  copy "$HERE/templates/CLAUDE.template.md" "$TARGET/CLAUDE.md"
  copy "$HERE/templates/AGENT_JOBS.template.md" "$TARGET/.claude/AGENT_JOBS.md"
fi
for s in "$HERE"/skills/*/; do copy "$s" "$TARGET/.claude/skills/$(basename "$s")"; done
echo "Done. Fill in CLAUDE.md and .claude/AGENT_JOBS.md, then tell Claude Code: start the next job and follow the loop in CLAUDE.md."
