# <PROJECT NAME> — agent job queue

Status values: `todo`, `doing`, `done`, `blocked` (waiting on something), `owner` (only a person can do it).
Work branch: `<work branch>`. Never push to `<deploy branch>`.

## Owner-only (agents must not attempt)

| ID | Task | Status |
|---|---|---|
| O1 | <backups, accounts, payments, approvals> | owner |

## Agent jobs

| ID | Job | Done when | Depends on | Status |
|---|---|---|---|---|
| J01 | <one feature> | <how to prove it is done> | — | todo |
