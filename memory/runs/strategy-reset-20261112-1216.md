# /strategy-reset run report — 2026-11-12 12:16

## Context that changed the run

This repository (`fahad21-nocode/visa-job-hunt`) did not contain a
career-ops workspace at all — only `sponsor_check.py` (a standalone
sponsor-register matcher) and its tests. None of the files the
`/strategy-reset` command expects to edit (`AGENTS.md`, `opencode.json`,
`.opencode/commands/daily.md`, `SETUP.md`, `career-ops-rules.md`,
`rules of cv creation.md`, `.claude/commands/sponsor-sweep.md`,
`memory/`, `outbox/`, or any auto-apply/auto-send script) existed in this
container. I confirmed this by searching the whole container filesystem,
not just the repo, and found nothing elsewhere either; no computer was
connected via Remote Control to check Fahad's own machine.

I raised this with Fahad before doing anything else. He chose: build the
workspace fresh in this repo, following strategy changes A–H, rather than
editing pre-existing files. Everything below reflects that green-field
build, not an edit of a prior "Sep 2026" version of this workspace.

## 1. Files changed (backup path)

Backup folder: `backups/strategy-reset-20261112-1216/`

- `.gitignore` — **edited** (backed up before editing). Added
  `!/opencode.json` so the new config file is tracked instead of being
  silently excluded by the existing root-level `/*.json` rule.

Everything else below is **new** — there was nothing to back up:

- `career-ops-rules.md`
- `rules of cv creation.md`
- `AGENTS.md`
- `SETUP.md`
- `opencode.json`
- `.opencode/commands/daily.md`
- `.claude/commands/sponsor-sweep.md`
- `memory/tracker.csv`, `backlog.csv`, `priority_employers.csv`,
  `contacts.csv`, `applications.csv`, `boards.csv`, `seen.jsonl`,
  `intel.md`, `decisions.md`, `memory/runs/` (this file)
- `outbox/README.md`

## 2. Changes A–H

| Change | Status | Note |
|---|---|---|
| A — auto-apply/auto-send off, weekly cap, backlog | **done** | No auto-send path existed to disable; built `auto_apply: false` / `auto_send: false` into `opencode.json`, cap of 10 in the same file, overflow routes to `memory/backlog.csv`. Draft-only language in `AGENTS.md` and `.opencode/commands/daily.md`. |
| B — tooling freeze until 17 Feb 2027 | **done** | In `career-ops-rules.md` §0, `AGENTS.md`, and `opencode.json.agent.tooling_freeze`. No Sep 2026 rule existed to supersede. |
| C — consultancy/outsourcer channel first | **done** | `memory/priority_employers.csv` seeded with the 15 named brands, `legal_entity`→`verified_on` blank for the agent to fill on each run; sweep order enforced in both `daily.md` and `sponsor-sweep.md`; `channel` column added to `tracker.csv`. |
| D — TSL window logic | **done** | `career-ops-rules.md` §4, `opencode.json.agent.apply_gate`, `TSL-WINDOW` tagging and countdown specified in both run commands; 1 Jan 2027 auto-reversion pre-logged in `memory/decisions.md`. |
| E — replace stale deadlines | **done** | No file in this repo ever stated 25 Sep 2026 or 30 Nov 2026 — confirmed by search (see §4 below). Correct dates (31 Dec 2026 / 17 Feb 2027 / mid-Jan 2027) were built in from the start; see Patched facts. |
| F — sponsorship question first | **done** | Standard question in `career-ops-rules.md` §8; `sponsor_confirmed` / `cos_by_date` columns in `tracker.csv`; close-on-written-no rule stated in §8 and both run commands. |
| G — warm intro before apply | **done** | `career-ops-rules.md` §9; `warm_path` column in `tracker.csv`; check against `contacts.csv` and `priority_employers.csv` required before preparing an application in both run commands. |
| H — R3/R4 as parallel tracks | **done** | Both run commands give R3 and R4 their own output section every run, alongside R1/R2, not a fallback. |

## 3. Patched facts (old value → new value, file)

Nothing in this repository stated a stale fact before this run — it had
no career-ops content at all. The following facts were written in
**already corrected**, so there was nothing to patch, but they're the
load-bearing numbers Fahad should double check against anything from an
older session elsewhere (e.g. his Windows workspace, if one exists):

- Application/CoS cut-off: **31 December 2026** (interim TSL CoS
  cut-off) — `career-ops-rules.md` §6, `opencode.json`.
- Sponsorship deadline: **17 February 2027** — same files; also the
  tooling-freeze lift date.
- Derived offer target: **mid-January 2027** (encoded as 2027-01-15 in
  `opencode.json`) — same files.
- Gate 2 screening number: new-entrant path (70% of going rate, floor
  £33,400) checked **before** the general £41,700 path — `career-ops-rules.md`
  §7, Gate 2.
- Gate 1: a parent's licence not covering a subsidiary is **unconfirmed,
  not failed**, and an overseas "Inc" can hold a UK licence — both
  written as the current (corrected) rule, not the retired one.

## 4. Anything not changed, and why

- No live auto-apply/auto-send script, cron job, scheduled task or
  n8n/Activepieces flow was found anywhere in this container to disable
  — there was nothing here to find. If one exists on Fahad's own
  machine, it is **not covered by this run** and still needs checking
  there.
- `opencode.json`'s schema is a workspace-local convention, not a
  verified OpenCode config format — flagged as such in the file's own
  `_comment`, since OpenCode's real schema wasn't available to check
  against in this container.
- Sponsor-register tools, `check_salary_threshold`, the Scrapling skill,
  and the job-board connectors are referenced but not installed or
  wired up here — adding any of them is itself gated by the tooling
  freeze (§0), so Fahad should approve that explicitly before it's done.

## 5. Rollback

Restore `.gitignore` from `backups/strategy-reset-20261112-1216/.gitignore`
to undo the one edit made to a pre-existing file. Delete the new files
listed in §1 to remove everything else this run added.
