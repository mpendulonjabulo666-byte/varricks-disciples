# What the team knows

Everything the owner has sent the team so far. Read this before you start. It is reference, not instructions for a specific job: the brief and the project's `CLAUDE.md` win when they differ.

## Who you work for
- Varrick builds apps, games, websites and the marketing for them, mostly alone, for his own products and for clients in South Africa.
- He often gives instructions by voice-to-text. Read them charitably and ask when a missing fact changes the result.
- Reply to him in English, in short plain sentences.
- Many of his users are on Android phones with limited data. Design and test for that first.
- Client websites for local businesses: WhatsApp is the main way to order or book, not a shopping cart. Never invent a business's hours, prices or details; ask the client.
- Nothing fake, ever. If you don't know, say so and say how to find out.

## 20 principles of UX and animation
From a reel by @charles.unemployed. The first twelve are the classic animation principles applied to interfaces; the rest are UX laws.
1. Squash and stretch
2. Anticipation: a small wind-up before the big move
3. Staging: direct the eye to the focus
4. Pose to pose
5. Follow through
6. Slow in and slow out
7. Move along arcs, not straight lines
8. Secondary action
9. Snappy timing
10. Exaggerated feedback
11. Solid drawing: give flat things depth and volume
12. Overall appeal
13. Fitts's law: bigger and closer targets are faster to hit
14. Bigger hit areas than the visible element
15. Hick's law: more choices, slower decisions
16. Miller's law: people hold about seven things at once, so chunk (a card number in groups of four)
17. Doherty threshold: respond within about 0.4 seconds or show progress
18. Postel's law: accept messy input, give clean output
19. Jakob's law: people expect your product to work like the ones they already know
20. Design for frequency of use: the thing done most often should be the easiest

For how to build motion well, read the `animate`, `emil-design-eng` and `animation-performance` skills in the index.

## Where to look for design references
From a reel by @ux.elena: OnePageLove, Fonts In Use, Httpster.net, Lapa.ninja, Bestwebsite.gallery, Designmadeingermany.de.
Look, learn the idea, then make something for this product. Never copy a page, its artwork or its text.

## Before launching an app: the legal list
From a reel by @sambutlerai ("How to not get sued when launching an app"). Use it as a checklist of things the owner must decide. It is not legal advice and the team is not a lawyer.
1. Privacy policy
2. Terms and conditions
3. GDPR compliance (for users in the EU). In South Africa the law is POPIA: health data needs explicit, separate consent and an Information Officer.
4. Cookie consent
5. Legal basis for each kind of data you process
6. Marketing consent
7. Data deletion
8. Data retention
9. Data processing agreements with the services you use
10. Third-party disclosure
11. Data security
12. Data breach procedure
13. Intellectual property
14. Open-source licences of what you ship
15. Payments and subscriptions
An agent may draft these documents. Only the owner (and a lawyer for anything that matters) approves them. A job that collects personal data is not done until the owner has answered the items that apply.

## Free tools and lists (check before promising anything; free tiers change)
- https://github.com/ripienaar/free-for-dev - services with a free tier (hosting, email, domains, AI).
- https://github.com/public-apis/public-apis - free APIs by category.
- https://github.com/xtool-org/xtool - build iOS apps from Linux or Windows.
- https://github.com/JustVugg/colibri - run very large open models on an ordinary machine.
- https://github.com/open-jarvis/OpenJarvis - personal AI on personal devices.
- https://github.com/INSANE0777/Awwwards-mcp - optional MCP server for studying award-winning sites.
- CodeRabbit - a GitHub app that reviews pull requests (price not checked).

## 19 principles of UX and animation, second list
From a reel by @bendoescare. It overlaps the list above. These seven are new. The meanings are the standard ones, not quotes from the reel.
1. Origin awareness: a thing opens from where the user touched, and closes back to it.
2. Staggering: items in a group enter one after another with a short delay, not all at once.
3. Rubber banding: past a limit, movement resists like an elastic band, then springs back.
4. Von Restorff effect: the one item that looks different is the one people remember.
5. Interruptible motion: the user can change their mind mid-animation and the interface follows at once.
6. Peak-end rule: people remember the best moment and the ending. Finish a flow on a win (a check mark, a short celebration).
7. Exaggeration: push a small cue a little further so the user notices it.

## Corner concentricity
From a reel by @guhmp4. When a rounded shape sits inside a rounded container, both corners share the same centre. Inner radius = outer radius minus the gap between them. If the gap is larger than the outer radius, the inner corner is square. Check it on cards, buttons in cards, images in frames and sheets.

## Architecture for a growing app
From a reel by @izzienjeri. Three ideas, used in this order, and only as far as the real problem needs. The reel itself says you do not need all of them.
1. Domain-driven design: start from the business parts (for example payments, accounts, refunds, notifications), not from the database tables. Each part owns its own rules.
2. Event-driven design: when something happens (a payment is made), the payment part publishes one event. Receipts, analytics and notifications each listen. The payment part does not call them.
3. Clean architecture: inside each part, keep the business rules free of framework and database code, and let the outer layers depend on the inner ones.
For NutriTale and the Vex app, start with step 1 on paper. Add events and layers only when two parts start to break each other.

## Marketing from evidence
From a reel by @jens.heitmann. The `reverse-engineer-marketing` skill (in the `marketing` pack, from coreyhaines31/marketingskills) builds a dated log of how another company grew from public evidence, compares it with the owner's own numbers, finds where they are weak and routes each play to another marketing skill. Rule for the marketer agent: use only public evidence, name every source, and never invent a competitor's numbers.

## Speed pass for a slow app
From a reel by @samro_ai. Five checks: find and fix every N+1 query, add indexes to searched columns, cache data that rarely changes, lazy-load images below the fold, make the interface respond at once to every click and fix up if the server says no. The owner already has a skill for this called `app-speed-pass`.

## Tools and lists seen in reels (link only, not skills)
- https://github.com/TauricResearch/TradingAgents (Apache-2.0): a research framework where several LLM agents play analyst, trader and risk roles. It is for study. It is not financial advice and it makes no promise of profit. Treat any trading result as unverified until it is back-tested with real data.
- https://github.com/n8n-io/n8n: workflow automation, self-hostable. Its licence is "fair-code", not an open-source licence, so the sync skips it. A reel said someone leaked thousands of n8n workflow templates. That claim was not checked. Do not import templates from an unknown source; read every node before you run one, because a workflow can send data out.
- https://github.com/affaan-m/ECC (MIT): a large agent setup with hundreds of skills. Only 22 chosen skills are in the `dev` pack. Adding all of them would flood the index and the agents would read the wrong one.

## Skills
`.claude/skills/INDEX.md` (or `~/.claude/skills/INDEX.md`) lists every installed skill. Read a skill only when the job matches it.
