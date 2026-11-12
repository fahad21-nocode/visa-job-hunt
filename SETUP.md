# SETUP.md

How this repository's career-ops workspace fits together, and what to run.

## What's here

- `sponsor_check.py` — standalone CLI that matches employer names against
  a downloaded Home Office sponsor-register CSV. See `README.md` for
  usage. Independent of everything below; the agent calls it (or the
  equivalent sponsor-register MCP tools, where available) as part of
  Gate 1 in `career-ops-rules.md`.
- `career-ops-rules.md` — the rules the agent follows. Read this before
  touching anything else.
- `rules of cv creation.md` — CV/cover-letter process.
- `AGENTS.md` — entry point for the OpenCode/OpenWork agent and Claude
  Code commands.
- `opencode.json` — config flags backing the rules (auto-apply/auto-send
  off, weekly cap, tooling freeze, apply-gate dates, sweep order).
- `.opencode/commands/daily.md`, `.claude/commands/sponsor-sweep.md` —
  the two run commands.
- `memory/` — pipeline state (tracker, backlog, contacts, applications,
  boards, priority employers, decisions log, intel notes, run reports).
- `outbox/` — drafted applications and outreach. Nothing in here is ever
  sent automatically.
- `backups/` — snapshots taken before each `/strategy-reset` run.

## Prerequisites

- Sponsor register tools (`check_sponsor_license`, `search_sponsors`,
  `get_sponsor_details`, or `sponsor_check.py` against a freshly
  downloaded register CSV).
- `check_salary_threshold` tool, or a live gov.uk check, for Gate 2.
- Scrapling skill, for visa-sponsorship searches.
- Connectors for LinkedIn, Indeed, ZipRecruiter, Dice and Glassdoor
  (scraping these directly is out of scope — see `career-ops-rules.md`
  §2).

None of the above are installed or wired up by this setup — adding one is
itself covered by the tooling freeze in `career-ops-rules.md` §0, so get
Fahad's explicit approval in-session before adding a scraper, board or MCP
server.

## Running a sweep

1. Read `AGENTS.md`, then `career-ops-rules.md`.
2. Run `.opencode/commands/daily.md` (OpenCode agent) or
   `.claude/commands/sponsor-sweep.md` (Claude Code, roles only, no CV
   work) in the sweep order they specify: priority employers, then
   TSL-window tagging, then the general sweep, then R3/R4 as parallel
   sections.
3. Update `memory/tracker.csv` and the other `memory/` files as you go.
   Never write to `outbox/` as a final step without it staying a draft.
4. Report advance rate per channel and per role family, and the R1/R3/R4
   sections, in the run summary.

## Memory files — minimum columns

- `tracker.csv`: role, employer, legal_entity, channel, route, rqf_level,
  tsl_window, soc_code, salary_advert, salary_new_entrant_min,
  salary_general_min, gate1, gate2, gate3, gate4, score, verdict,
  sponsor_confirmed, cos_by_date, warm_path, applied_date, status, notes
- `backlog.csv`: role, employer, channel, route, score, rank, added_date,
  reason_over_cap
- `priority_employers.csv`: brand, legal_entity, register_match, rating,
  route, careers_url, ats, verified_on, notes
- `contacts.csv`: name, role, employer, relationship, warm_path,
  email_status, last_contacted, notes
- `applications.csv`: role, employer, date_prepared, date_approved,
  date_submitted, submitted_by, outbox_path, status
- `boards.csv`: board_name, type, scraping_allowed, connector, notes
- `seen.jsonl`: one JSON object per seen job posting, append-only, for
  dedup.

## Rollback

Every `/strategy-reset` run backs up every file it is about to edit to
`backups/strategy-reset-<YYYYMMDD-HHMM>/` before editing it. To undo a
run, copy that folder's contents back over the working tree.
