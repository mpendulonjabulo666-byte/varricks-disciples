#!/usr/bin/env bash
# Copies the team and its skills into a project.
#
#   ./install.sh /path/to/project                      generic team, skill pack: core
#   ./install.sh /path/to/project nutritale            saved NutriTale team, packs: core,design,security
#   ./install.sh /path/to/project nutritale --user     same, but skills go to ~/.claude/skills (not into the repo)
#   ./install.sh /path/to/project --packs all          every pack (core design security video extras)
#   ./install.sh /path/to/project --update-skills      replace skills already installed with the repo's newer copies
#
# Agents, CLAUDE.md and the job list are never overwritten. Skills are only replaced with --update-skills.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET=""; PROFILE=""; PACKS=""; USER_MODE=0; UPDATE=0
while [ $# -gt 0 ]; do
  case "$1" in
    --packs) PACKS="${2:?--packs needs a list, e.g. core,design}"; shift 2 ;;
    --user) USER_MODE=1; shift ;;
    --update-skills) UPDATE=1; shift ;;
    --*) echo "Unknown option: $1"; exit 1 ;;
    *) if [ -z "$TARGET" ]; then TARGET="$1"; else PROFILE="$1"; fi; shift ;;
  esac
done
[ -n "$TARGET" ] || { echo "Give the path to your project"; exit 1; }
[ -d "$TARGET" ] || { echo "Not a folder: $TARGET"; exit 1; }
if [ -z "$PACKS" ]; then
  if [ "$PROFILE" = "nutritale" ]; then PACKS="core,design,security"; else PACKS="core"; fi
fi
if [ "$PACKS" = "all" ]; then
  PACKS="$(cd "$HERE/skills" && for d in */; do [ -f "$d/INDEX.tsv" ] && printf '%s,' "${d%/}"; done)"; PACKS="${PACKS%,}"
fi
has_pack() { case ",$PACKS," in *",$1,"*) return 0 ;; *) return 1 ;; esac; }

if [ "$USER_MODE" = 1 ]; then SK="$HOME/.claude/skills"; SKREF="~/.claude/skills"; else SK="$TARGET/.claude/skills"; SKREF=".claude/skills"; fi
mkdir -p "$TARGET/.claude/agents" "$SK"

copy() { # never overwrite a file that is already there
  if [ -e "$2" ]; then echo "kept (already exists): $2"; else cp -r "$1" "$2"; echo "added: $2"; fi
}
copy_agents() { # $1 = folder of agents
  for f in "$1"/*.md; do
    b="$(basename "$f")"
    case "$b" in *designer.md) has_pack design || { echo "skipped $b (design pack not installed)"; continue; } ;; esac
    copy "$f" "$TARGET/.claude/agents/$b"
  done
}
if [ -n "$PROFILE" ]; then
  P="$HERE/projects/$PROFILE"; [ -d "$P" ] || { echo "No such project team: $PROFILE"; exit 1; }
  copy_agents "$P/agents"
  copy "$P/CLAUDE.md" "$TARGET/CLAUDE.md"
  copy "$P/AGENT_JOBS.md" "$TARGET/.claude/AGENT_JOBS.md"
else
  copy_agents "$HERE/agents"
  copy "$HERE/templates/CLAUDE.template.md" "$TARGET/CLAUDE.md"
  copy "$HERE/templates/AGENT_JOBS.template.md" "$TARGET/.claude/AGENT_JOBS.md"
fi

# skills: flat folders in .claude/skills/<name>/ so Claude Code finds them
IFS=',' read -ra PK <<< "$PACKS"
for p in "${PK[@]}"; do
  [ -d "$HERE/skills/$p" ] || { echo "No such skill pack: $p"; exit 1; }
  for s in "$HERE/skills/$p"/*/; do
    [ -f "$s/SKILL.md" ] || continue
    n="$(basename "$s")"
    if [ "$UPDATE" = 1 ] && [ -e "$SK/$n" ]; then rm -rf "$SK/$n"; echo "replaced: $SK/$n"; fi
    copy "$s" "$SK/$n"
  done
done

# INDEX.md lists every skill that is installed, so agents can find new ones without any edit
{
  echo "# Installed skills"
  echo
  echo "Read a skill's SKILL.md only when your job matches its description. Packs installed: $PACKS."
  echo
  echo "| Skill | Use when | File |"
  echo "|---|---|---|"
  for p in "${PK[@]}"; do
    [ -f "$HERE/skills/$p/INDEX.tsv" ] || continue
    awk -F'\t' -v ref="$SKREF" '{ printf "| %s | %s | %s/%s/SKILL.md |\n", $1, $2, ref, $1 }' "$HERE/skills/$p/INDEX.tsv"
  done
} > "$SK/INDEX.md"
echo "wrote: $SK/INDEX.md"
echo "Done. Fill in CLAUDE.md and .claude/AGENT_JOBS.md, then tell Claude Code: start the next job and follow the loop in CLAUDE.md."
