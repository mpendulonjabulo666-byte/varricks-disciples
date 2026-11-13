# Varrick's disciples

A small agent team for Claude Code, for every build: apps, games, websites and the marketing for them. One planner hands out jobs. Cheap, fast workers do them. A stronger reviewer checks every change before it counts as done. The workers can use a shelf of skills, and the shelf keeps itself up to date from your forked repos.

## The team

| Agent | Model | Job |
|---|---|---|
| Orchestrator (your main session) | your main model | Plans, hands out one job at a time, checks every result |
| `teacher` | Sonnet | Turns your rough request or voice note into clear jobs and briefs for the others. Asks you when a fact is missing. |
| `scout` | Haiku | Read-only. Finds where the code lives. |
| `builder` | Haiku | Makes the change for one job and commits it. |
| `designer` | Sonnet | Makes the change for jobs marked UI (layout, CSS, motion, phone feel). Only installed with the design skills. |
| `marketer` | Sonnet | Writes landing copy, posts, captions, WhatsApp messages and store text. Drafts only; you send. |
| `tester` | Haiku | Writes the test and runs all tests. |
| `reviewer` | Opus | Read-only. Says PASS or FAIL against the brief, the rules and the quality bar. |

No agent uses Fable. To change a model, edit the `model:` line at the top of the agent's file.

## What is in this repo

| Path | What it is |
|---|---|
| `agents/` | The generic agents. They work in any project. |
| `knowledge/KNOWLEDGE.md` | What the team knows: who it works for, the house rules, and everything you have sent (UX and animation principles, reference sites, the launch legal list, free tools). Installed as `.claude/KNOWLEDGE.md`. To teach the team something new, add it here and re-install with `--update-skills`. |
| `knowledge/QUALITY_BAR.md` | The no-slop bar for interfaces, words and code. The reviewer fails any job that breaks it. Installed as `.claude/QUALITY_BAR.md`. |
| `PHONE.md` | How to get approval prompts on your phone and answer them there. |
| `templates/` | A `CLAUDE.md` and a job queue to fill in for a new project. |
| `skills/<pack>/<skill>/` | The skill shelf, in packs (below). `skills/CATALOG.md` lists every skill, where it came from, its licence and commit. |
| `skills.sources.json` | Which repos the skills come from. |
| `scripts/sync_skills.py` | Pulls new and changed skills from those repos. |
| `projects/nutritale/` | The team as set up for the NutriTale app: its rules, agents and 20 jobs. |
| `templates/mcp.awwwards.json` | Optional: the Awwwards inspiration server (see "Not skills"). Not installed by default. |
| `install.sh` | Copies the team and skills into a project. |

## Skill packs

| Pack | What | Installed by default |
|---|---|---|
| `core` | Plan-before-you-build and commit-message skills | every project |
| `design` | Layout, motion, brand, phone feel, spec drawings, product demos | every project |
| `security` | Code-security review skills (Strix). For reading, not for attacking anything. | every project |
| `video` | Launch videos and motion (brag, hyperframes, claude-video, and any other fork that passes the licence check) | no |
| `extras` | Other skills from your forks | no |

## How the agents find skills

`install.sh` writes `.claude/skills/INDEX.md`: one line per installed skill, with when to use it. Agents open the index, then read only the skill that matches the job. Because the agents read the index and not a fixed list, a skill added by the next sync reaches them with no edit to any agent file. Only `impeccable` and `contextual-commit` are preloaded into the designer.

## Use it in a project

```bash
git clone https://github.com/mpendulonjabulo666-byte/varricks-disciples
cd varricks-disciples
./install.sh /path/to/your/project                    # the whole team + core, design and security skills
./install.sh /path/to/repo nutritale --user           # NutriTale team; skills go to ~/.claude/skills, not into the repo
./install.sh /path/to/project --packs all             # every pack
```

Why `--user` for NutriTale: that repo deploys by FTP. Keep megabytes of skill files out of it. The agents read `~/.claude/skills/INDEX.md` when the project has none.

Then fill in `CLAUDE.md` (deploy branch, work branch, test command), write jobs in `.claude/AGENT_JOBS.md`, and tell Claude Code: "Start the next job in .claude/AGENT_JOBS.md and follow the loop in CLAUDE.md."

## Keep the skills up to date

```bash
python3 scripts/sync_skills.py                  # all sources
python3 scripts/sync_skills.py --only impeccable
python3 scripts/sync_skills.py --sync-forks     # first refresh your forks from their upstream (needs `gh auth login`)
git diff --stat                                 # READ what changed
git add -A && git commit -m "Update skills"
./install.sh /path/to/project --update-skills   # copy the newer skills into a project
```

Needs `git` and `python3`. What the sync does for each repo in `skills.sources.json`:
- It finds every folder with a `SKILL.md` under the repo's `roots`. A new skill upstream is picked up with no edit here.
- It checks the repo's licence file. No licence, or one that is not MIT, Apache-2.0, ISC, BSD or Unlicense: the skill is skipped and the repo is only linked.
- It copies the skill with its licence and notice files. Pictures, fonts, audio, video and files over 2 MB are left out (the count is in `CATALOG.md`), so a skill that depends on its bundled photos will be missing them.
- It writes `skills/LOCK.json` (commit and content hash) so you can see exactly what changed.

To add a repo, add an entry to `skills.sources.json`: `roots` for a folder of skills, or `skills` for one skill at a known path.

**Read the diff before you commit.** A skill is instructions and sometimes scripts written by someone else, and your agents will follow them. The sync prints a `? review` line when it sees `curl … | sh`, `wget … | sh` or `rm -rf /`; that is a hint, not a security scan. If a repo's owner changes a skill in a bad way, the diff is where you catch it.

The sync has been run against the repos in `skills.sources.json`. `--sync-forks` has not been tested (it needs your GitHub login on your own machine). The GitHub fork of a repo does not change what the sync pulls: it reads the repo named in the manifest (your fork where `"fork": true`, otherwise the original).

## Not skills (links only)

These came from the reels. They are tools or lists, not skills, so nothing is copied.

| Repo | What it is |
|---|---|
| [xtool-org/xtool](https://github.com/xtool-org/xtool) (MIT) | "Cross-platform Xcode replacement": builds and deploys iOS apps with SwiftPM from Linux, Windows or macOS. Read https://xtool.sh before relying on it for the NutriTale iPhone app; what an Apple account and App Store release need was not checked. |
| [JustVugg/colibri](https://github.com/JustVugg/colibri) (Apache-2.0, already forked) | Runs very large open models on an ordinary machine by keeping the active part in RAM and reading the rest from disk. Pure C, no GPU. Useful reading for your quantization learning. |
| [open-jarvis/OpenJarvis](https://github.com/open-jarvis/OpenJarvis) (Apache-2.0) | "Personal AI, on personal devices" (Stanford project). Python 3.10+. |
| [ripienaar/free-for-dev](https://github.com/ripienaar/free-for-dev) | A list of services with a free tier (hosting, email, domains, AI and more). The repo has no licence file, so it is link only. Free tiers change: check each service before you promise a client anything. |
| [public-apis/public-apis](https://github.com/public-apis/public-apis) (already forked) | A list of free APIs, organised by category. |
| [INSANE0777/Awwwards-mcp](https://github.com/INSANE0777/Awwwards-mcp) (MIT) | An MCP server, not a skill: it lets an agent look at award-winning sites and measure their colours, type and motion. Optional, off by default. Install line from its README (needs Node 22.13+): `claude mcp add awwwards -- npx -y awwwards-mcp`. `templates/mcp.awwwards.json` has the same as a project config. Use it to learn from a site, never to copy someone's page for a client. |
| immich, Nextcloud, Pi-hole | Self-hosted apps (photos, files, ad blocking). Nothing for the agents; only relevant if you ever run your own server. |
| CodeRabbit | A GitHub app that reviews pull requests. It has no repo to fork. Its price and free tier were not checked. |

## Rules the team always keeps

- Never push to a branch that deploys. Only the owner merges.
- Never touch secrets or deploy workflows.
- One job, one feature, one commit, one test.
- No invented data and no invented test results.
- When unsure, stop and ask.

## Limits

- Haiku workers are fast and cheap, and they make more mistakes than a bigger model. That is why the reviewer and the orchestrator check everything.
- The team is only as good as the job list. A vague job gets a vague result.
- The quality bar and the teacher are instructions, not a guarantee. They raise the floor; you still look at the result.
- The team has not been run on a full job yet. Start with one small job and read the result yourself.
- Skills preloaded through an agent's `skills:` line are documented behaviour, but Claude Code versions differ. If the designer does not seem to know `impeccable`, tell it to Read `.claude/skills/impeccable/SKILL.md` (or the `~/.claude/skills/` copy).

## Credits

Every skill keeps the licence file from its source repo. The full list, with repo, licence and commit, is in `skills/CATALOG.md`. Skills come from the repos of Emil Kowalski, Paul Bakaus (Impeccable), Leonxlnx (taste-skill), Enes Ozturk (dimensional-drawing), oil-oil (oil-ui), Fatih Aydost (brand-identity), Benji Taylor (stageshow), Strix, Hyperframes, brag and the other forks listed in `skills.sources.json`. The planner-and-workers idea comes from a reel by @murphmaxxing.
