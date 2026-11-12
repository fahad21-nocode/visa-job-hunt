# AGENTS.md — career-ops operating instructions

This file is the entry point for the OpenCode/OpenWork agent running on
Fahad's machine, and for Claude Code commands invoked in this repository.
Built by `/strategy-reset` on 2026-11-12 as a green-field workspace — no
earlier version of this file existed here.

## Read these first, in order

1. `career-ops-rules.md` — wins on rules. Gates, routes, apply gate,
   tooling freeze, dates, channel priority, TSL logic.
2. `rules of cv creation.md` — CV/cover-letter process. Only invoked when
   a CV is actually being written; `/sponsor-sweep` never invokes it.
3. `opencode.json` — machine-readable config (caps, flags, dates) backing
   the rules above. If the two ever disagree, `career-ops-rules.md` wins
   and `opencode.json` needs patching.

## Hard constraints (non-negotiable, not just defaults)

- **Never submit an application or send a message without Fahad's
  per-item approval.** `auto_apply: false` and `auto_send: false` in
  `opencode.json`. The agent prepares applications and drafts outreach to
  `outbox/` only. Fahad approves and submits each one himself, manually
  and staggered.
- **Weekly cap: 10 fully tailored applications.** Anything above the cap
  for the week goes to `memory/backlog.csv`, ranked — it is not dropped.
- **Tooling freeze until 17 February 2027.** No new agents, model layers,
  scrapers, boards or MCP servers unless Fahad explicitly approves in the
  session. Fix only what's broken.
- **Never assert a SOC code, a going rate or a sponsor licence from
  memory.** Always verify at run time: sponsor register tools,
  `check_salary_threshold`, gov.uk.
- **Plain figures only.** No "c.", "circa", "around", "approx." or "~"
  before a number, anywhere — CVs, outreach, run output.

## Which workflow to run

| Request | Do this |
|---|---|
| Daily/weekly sweep | `.opencode/commands/daily.md` |
| Find sponsoring roles only (no CV work) | `.claude/commands/sponsor-sweep.md` |
| Assess / score / screen a role or employer | Four-gate framework, `career-ops-rules.md` §7 |
| Salary or visa-threshold question | `career-ops-rules.md` §7 Gate 2: new-entrant path first, general path second |
| CV, resume, tailoring, ATS check | `rules of cv creation.md`, five stages in order |
| Outreach, follow-up, recruiter message | `career-ops-rules.md` §10, draft only |

## Sweep order (every sweep, daily or sponsor-sweep)

1. `memory/priority_employers.csv` — the consultancy/outsourcer channel
   (`career-ops-rules.md` §3).
2. TSL-window tagging pass over RQF 3–5 roles (`career-ops-rules.md` §4).
3. General register-first sweep across all eleven role families.
4. R3 and R4 as parallel tracks alongside R1 — their own section in every
   run summary, not a fallback checked only when R1 is thin
   (`career-ops-rules.md` §2).

## Key dates

- **31 December 2026** — interim TSL CoS cut-off.
- **17 February 2027** — sponsorship must be in place; tooling freeze
  lifts.
- **Mid-January 2027** — derived working target: offer in hand by this
  point.

On 1 January 2027 the agent reverts the RQF 3–5 apply gate from 3.5/5 to
4.0/5 on its own and logs it in `memory/decisions.md`. This is a standing
instruction, not something to wait to be asked for.

## Sourcing constraints

- Use the Scrapling skill for visa-sponsorship searches.
- Never scrape LinkedIn, Indeed, ZipRecruiter, Dice or Glassdoor — use
  their connectors.
- UK-wide scope, including government employers, the NHS, Civil Service
  Jobs and NHS Jobs.
- No 12-month fixed-term contracts.

## Workspace layout

- `memory/` — tracker, backlog, contacts, applications, boards, priority
  employers, decisions log, intel notes, run reports. Source of truth for
  pipeline state.
- `outbox/` — drafted applications and outreach, never auto-sent.
- `backups/` — pre-edit snapshots taken by `/strategy-reset` runs.
