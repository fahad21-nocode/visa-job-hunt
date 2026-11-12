---
description: Find sponsor-eligible roles only. Never drafts a CV or cover letter.
---

# /sponsor-sweep

Finds roles only. Read `AGENTS.md` and `career-ops-rules.md` first. This
command never invokes `rules of cv creation.md` and never writes a CV,
cover letter or application answer — if asked to do that inline, say that
`/sponsor-sweep` doesn't do CV work and point to the CV workflow in
`AGENTS.md` instead.

## Hard constraints

- Never submit an application or send a message — this command only
  finds and scores roles, and may prepare a draft into `outbox/`. Nothing
  it touches is sent without Fahad's per-item approval.
- Tooling freeze in force until 17 Feb 2027 (`career-ops-rules.md` §0).
- Never assert a SOC code, going rate or sponsor licence from memory —
  verify every time with the sponsor-register tools / `check_salary_threshold`
  / gov.uk.
- Use the Scrapling skill for visa-sponsorship searches. Never scrape
  LinkedIn, Indeed, ZipRecruiter, Dice or Glassdoor — use their
  connectors.
- UK-wide scope, including government employers, the NHS, Civil Service
  Jobs and NHS Jobs. No 12-month fixed-term contracts.

## Sweep order

1. **Priority employers.** Sweep `memory/priority_employers.csv` first —
   the consultancy/outsourcer channel (`career-ops-rules.md` §3). Resolve
   any blank `legal_entity`..`verified_on` fields via Gate 1 before
   scoring. Search this channel's priority keywords (SuccessFactors
   support/AMS, HRIS support, HR operations analyst, application support
   analyst, service desk analyst, graduate/associate consultant (HR
   tech/SAP/ERP), people systems).
2. **TSL-window tagging.** For every RQF 3–5 role, verify TSL/ISL
   occupation status and employer CoS-issuance plausibility at run time
   (`career-ops-rules.md` §4). Tag `TSL-WINDOW`, surface first, show the
   countdown to 31 December 2026.
3. **General register-first sweep.** All eleven role families
   (`career-ops-rules.md` §2), routes R1 and R2.
4. **R3 and R4 — parallel tracks.** Their own output section every run,
   not a fallback.

## Per role

- Run the four-gate framework and apply gate (`career-ops-rules.md` §5,
  §7). State route, gate-by-gate evidence, dual-path salary result,
  score /5, verdict.
- Check `memory/contacts.csv` and `memory/priority_employers.csv` for a
  warm path before treating the role as ready to prepare; record
  `warm_path` in `memory/tracker.csv`.
- Record `channel` (`consultancy` / `in-house` / `agency` / `public
  sector`) in `memory/tracker.csv`.
- If this is first contact, include the sponsorship question
  (`career-ops-rules.md` §8) in the drafted note and record
  `sponsor_confirmed` / `cos_by_date`. Close the row on a written "no".
- Respect the weekly cap in `opencode.json`
  (`agent.weekly_application_cap`); anything over cap goes to
  `memory/backlog.csv`, ranked, not dropped.

## Output

Role list grouped `TSL-WINDOW` first, then by channel, with route, score,
verdict, warm path and sponsor-confirmation status. Separate sections for
R3 and R4. Advance rate per channel and per role family. No CV, cover
letter or application answer appears in this command's output.
