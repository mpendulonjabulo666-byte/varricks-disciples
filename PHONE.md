# Approve from your phone

Claude Code has this built in. It is called Remote Control. The agents keep running on the computer; your phone shows the same session, and permission prompts and questions come to the phone as notifications. Source: https://code.claude.com/docs/en/remote-control (read 13 Nov 2026).

## What you need
- A Pro, Max, Team or Enterprise plan, signed in with `/login`. It does not work with an API key.
- The Claude app on your Android phone, signed in to the same account.
- The computer must stay on, online, with Claude Code open. The phone is a window into that session. It is not a second computer.

## Set it up once
1. In the project folder run `claude`, then type `/remote-control` (or `/rc`). Or start with `claude remote-control`.
2. Scan the QR code with your phone (in `claude remote-control`, press space to show it). The session opens in the Claude app. It is also listed at claude.ai/code.
3. On the phone, allow notifications for the Claude app when Android asks.
4. On the computer, run `/config` and turn on **Push when actions required** (permission prompts and questions). **Push when Claude decides** adds a notification when a long job finishes.

After that: start a job, walk away, tap the notification, tap Allow or Deny.

## Good to know
- Notifications are skipped while you are typing in the terminal on the computer.
- If the laptop sleeps or the network drops, the session reconnects when it is back.
- Other people have reported cases where approving on the phone did not reach the computer. If a prompt seems stuck, answer it on the computer and update Claude Code.
- Do not use `--dangerously-skip-permissions` to avoid prompts. The prompts are how you stop an agent before it does something you did not want.
- This has not been tested on your phone yet. Try it once on a small job first.
