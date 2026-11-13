# <PROJECT NAME> — how to work here

<One or two lines: what the project is, the language, where the code lives. Name the docs to read first.>

## Hard rules (every agent, every job)

1. **Deploy branch:** `<branch>` deploys to the live site. Never push to it. Work on `<work branch>`. Only the owner merges.
2. Never read, print, edit or commit secrets, key files or CI/deploy workflows.
3. One job = one feature = one commit.
4. Every job adds or extends a test. Test command: `<command>`. A job is not done while any test fails.
5. Nothing fake: no invented data or test results. If data is missing, stop and report.
6. If a job is unclear or blocked, stop and report. Do not guess.
<Add the project's own safety rules here.>

## Team setup (planner + workers)

The main session is the **orchestrator**. It plans, hands out one job at a time, and checks every result. It does not write feature code itself.

| Agent | Model | Job |
|---|---|---|
| `scout` | haiku | Read-only. Finds where the logic lives. |
| `builder` | haiku | Makes the change for one job and commits it. |
| `tester` | haiku | Writes the test, runs all tests, reports the raw output. |
| `reviewer` | same as main session | Read-only. Says PASS or FAIL. |

## The loop for each job in `.claude/AGENT_JOBS.md`

1. Orchestrator picks the next `todo` job that is not `blocked` or `owner`.
2. `scout` reports the current code for that job.
3. Orchestrator writes a short brief: goal, files, done-when, what not to touch.
4. `builder` makes the change.
5. `tester` adds the test and runs every test.
6. `reviewer` reviews the diff. FAIL goes back to step 4 with the reasons (max 3 rounds, then stop and tell the owner).
7. Orchestrator re-runs the tests itself and sets the job to `done`.

Jobs that touch different files may run in parallel. Jobs that touch the same file run one after the other.
