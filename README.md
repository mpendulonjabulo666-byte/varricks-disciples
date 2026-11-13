# Varrick's disciples

A small agent team for Claude Code. One planner hands out jobs. Cheap, fast workers do them. A stronger reviewer checks every change before it counts as done.

## The team

| Agent | Model | Job |
|---|---|---|
| Orchestrator (your main session) | your main model | Plans, hands out one job at a time, checks every result |
| `scout` | Haiku | Read-only. Finds where the code lives. |
| `builder` | Haiku | Makes the change for one job and commits it. |
| `tester` | Haiku | Writes the test and runs all tests. |
| `reviewer` | same as main | Read-only. Says PASS or FAIL. |

## What is in this repo

| Path | What it is |
|---|---|
| `agents/` | The four generic agents. They work in any project. |
| `templates/` | A `CLAUDE.md` and a job queue to fill in for a new project. |
| `skills/` | Two skills the team uses (see credits). |
| `projects/nutritale/` | The team as set up for the NutriTale app: its rules, agents and 20 jobs. |
| `install.sh` | Copies the team into a project. It never overwrites a file that already exists. |

## Use it in a project

```bash
git clone https://github.com/mpendulonjabulo666-byte/varricks-disciples
./varricks-disciples/install.sh /path/to/your/project
```

Then:
1. Open `CLAUDE.md` in your project and fill in the deploy branch, the work branch and the test command.
2. Write your jobs in `.claude/AGENT_JOBS.md`. Each job needs a "done when".
3. In Claude Code say: "Start the next job in .claude/AGENT_JOBS.md and follow the loop in CLAUDE.md."

For NutriTale, use the saved team: `./install.sh /path/to/repo nutritale`

## Rules the team always keeps

- Never push to a branch that deploys. Only the owner merges.
- Never touch secrets or deploy workflows.
- One job, one feature, one commit, one test.
- No invented data and no invented test results.
- When unsure, stop and ask.

## Limits

- Haiku workers are fast and cheap, and they make more mistakes than a bigger model. That is why the reviewer and the orchestrator check everything.
- The team is only as good as the job list. A vague job gets a vague result.
- It has not been run on a full job yet. Start with one small job and read the result yourself.

## Credits

- `skills/pre-impl-discussion` was copied from the `page-agent` fork (MIT licence, copyright SimonLuvRamen). The licence file is in the folder.
- `skills/contextual-commit` was copied from the `repomix` fork (MIT licence, copyright Kazuki Yamada). The licence file is in the folder.
- The planner-and-workers idea comes from a reel by @murphmaxxing.
