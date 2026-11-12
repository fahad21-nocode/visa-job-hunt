# Career-ops rules

Fahad's standing rules for this job search. This file wins on **rules** over any
skill, prompt or model habit. On **facts** (live roles, dates, thresholds, his
experience), the most recently stated version wins — if a later message
supersedes a fact in this file, use the later fact and say out loud that this
file needs patching. Never change a fact silently.

Created by `/strategy-reset` on 2026-11-12, green-field (no prior career-ops
workspace existed in this repository). See `memory/runs/` for the run report.

## 0. Tooling freeze (in force until 17 Feb 2027)

No new agents, model layers, scrapers, boards or MCP servers unless Fahad
explicitly approves in the session. Fix only what's broken. This supersedes
any earlier rule that let the agent install tools or change config without
asking — no such rule exists yet in this workspace, so this is the only
rule that has ever applied here.

## 1. Never send, never submit automatically

- `auto_apply` and `auto_send` are `false` in `opencode.json`. No script,
  cron job, scheduled task or flow in this workspace submits an application
  or sends a message without Fahad's per-item approval. If one is ever
  added, it must ship with `auto_apply: false` / `auto_send: false` (or be
  commented out with a dated `# disabled by /strategy-reset` note) and the
  tooling freeze in §0 applies to adding it at all.
- The agent prepares applications and drafts outreach to `outbox/` only.
  Fahad approves and submits each one himself. Outreach is drafted, never
  sent, and he sends it manually and staggered — one at a time, never a
  batch landing at the same time.
- **Weekly cap: 10 fully tailored applications** (config value
  `weekly_application_cap` in `opencode.json`, changeable by Fahad). Volume
  above the cap goes to `memory/backlog.csv`, ranked by score, not dropped.

## 2. Scope and routes

Eleven role families are in scope: automation/integration, AI-LLM
implementation, business systems & application support, data & reporting
analysis, HR systems/HRIS, broader HR/people operations, service & customer
operations, project/delivery/PMO, recruitment/talent operations,
revenue/CRM operations, technical customer-facing SaaS.

Scope is UK-wide, including government employers, the NHS, Civil Service
Jobs and NHS Jobs.

Four routes, run in parallel, not as a fallback chain:
- **R1** — sponsored UK
- **R2** — non-sponsored UK
- **R3** — remote for an India base, or in-office India (GCC HR-tech or
  founding-stage AI startup roles), employer anywhere
- **R4** — Gulf/international

Sponsorship is a **router, not a filter**: broaden discovery, narrow
application. The apply gate (§5) still applies.

Ruled out: 12-month fixed-term contracts.

Sourcing constraints (standing, unchanged by this reset):
- Use the Scrapling skill for visa-sponsorship searches.
- Never scrape LinkedIn, Indeed, ZipRecruiter, Dice or Glassdoor — use
  their connectors.
- `/sponsor-sweep` finds roles only. It never drafts CVs.

## 3. Priority channel: consultancies and outsourcers first

The highest-probability sponsor channel — IT consultancies and
outsourcers (SuccessFactors/HCM implementation and AMS partners,
Big-4/SI graduate and associate consultant pipelines) — is swept **first**,
before the general register-first sweep.

- `memory/priority_employers.csv` holds the seeded brand list. `legal_entity`
  through `verified_on` start blank; the agent fills them on each run using
  Gate 1 rules below (resolve legal entity first, check both register
  tools, compare name/number/location, reject fuzzy matches under 5
  characters, treat parent ≠ subsidiary coverage as unconfirmed not failed
  unless linked).
- Priority role keywords for this channel: SuccessFactors support/AMS,
  HRIS support, HR operations analyst, application support analyst,
  service desk analyst, graduate/associate consultant (HR tech, SAP, ERP),
  people systems. The other eleven role families (§2) stay in scope,
  ranked below this channel.
- `memory/tracker.csv` has a `channel` column (`consultancy` / `in-house` /
  `agency` / `public sector`). Every run summary reports the advance rate
  per channel and per role family.
- `.opencode/commands/daily.md` and `.claude/commands/sponsor-sweep.md`
  both sweep `priority_employers.csv` before the general sweep.

## 4. Interim Temporary Shortage List (TSL) window

The certificate of sponsorship for an RQF 3–5 role must be issued before
**31 December 2026** to use the interim Temporary/Immigration Shortage List
easing. For any RQF 3–5 role:

- Verify at run time — never from memory — that the occupation is on the
  current TSL/ISL (gov.uk Appendix Skilled Occupations), using the
  sponsor-register and salary-threshold tools plus a live gov.uk check.
- Also check the employer can realistically issue a CoS by mid-December:
  large sponsor, in-house immigration team, fast hiring process.
- After 31 December 2026, RQF 3–5 roles score only against whatever
  replacement list is published then. Do not assume the old list carries
  over — re-verify, don't assume.
- Tag qualifying roles `TSL-WINDOW`, show them first in run output, and
  show a countdown in days to 31 December 2026.

Apply gate while the window is open:
- RQF 3–5 roles: **3.5/5** until 31 December 2026.
- RQF 6+ roles: **4.0/5**, unchanged.
- On 1 January 2027 the agent reverts the RQF 3–5 gate to 4.0/5 on its own
  and logs the change in `memory/decisions.md`. `opencode.json` encodes
  both gate values and the switch date so this happens without a
  judgement call.

## 5. Apply gate

Score every role against the four-gate framework (§7), then give a verdict
against the apply gate:
- **4.0/5** — general default.
- **3.5/5** — RQF 3–5 roles only, until 31 December 2026 (§4).

State which route (R1–R4) a role sits on. For R2/R3/R4 roles, Gates 1, 2
and 4 may not apply — say so explicitly rather than skipping silently.

## 6. Key dates (patched 12 Nov 2026 — see run report for old values)

- **31 December 2026** — interim TSL CoS cut-off (§4).
- **17 February 2027** — sponsorship must be in place (Fahad's stated
  deadline; this is also when the tooling freeze in §0 lifts).
- **Mid-January 2027** — derived working target: offer in hand by this
  point, to leave runway for CoS issuance and visa processing before
  17 Feb 2027.

Any file or draft in this workspace that states a different application
cut-off or CoS target is wrong — flag it rather than copying it forward.

## 7. Four-gate screening framework

### Gate 1 — Sponsor licence
Requirement: an A-rated Skilled Worker licence on the Home Office register.
- Resolve the trading/brand name to the registered legal entity name first
  (Companies House, company website footer, terms page), then search the
  register. Use both `check_sponsor_license` and `search_sponsors`;
  follow up with `get_sponsor_details`.
- Compare name, Companies House number and location before treating a hit
  as a match — fuzzy matching returns parents for subsidiaries and
  look-alikes in other towns.
- A parent's licence covers a subsidiary **only if** that subsidiary has
  been added to it as a linked branch. If the hiring entity isn't on the
  register but its parent is, score Gate 1 as **unconfirmed, not failed**.
  Written confirmation from the employer settles Gates 1 and 4 together.
- Reject fuzzy matches on names under 5 characters.
- An overseas "Inc" can hold a UK licence through its UK establishment —
  search for the exact entity that would employ him rather than assuming
  either way.
- Check the rating is A, not B, and that the route includes Skilled
  Worker. Treat any local copy of the register as possibly stale.

### Gate 2 — Occupation code and salary (new-entrant path first)
Fahad qualifies as a new entrant through the Graduate visa switch. Check
**both** paths and pass if either qualifies:
1. **New entrant (primary):** 70% of the role's going rate for its SOC
   code, minimum **£33,400**, pro-rated to real weekly hours. £33,400 is a
   floor, not a flat number — it only binds where 70% of the going rate
   falls below it.
2. **General (secondary):** £41,700 or the occupation going rate,
   whichever is higher.
3. **Immigration Salary List variant**, as a third path, if the occupation
   is on it.
- Never assert a SOC 2020 code, going rate or threshold from memory —
  verify every time with `check_salary_threshold` and gov.uk, using the
  role's real weekly hours.
- If the tool's title-to-SOC mapping looks implausible, retry with a
  closer job title or check gov.uk directly, and label the result
  "not tool-verified" if you still can't confirm it.
- Verify the new-entrant visa conditions on gov.uk each run, not from
  memory (UK presence on Student/Graduate visa route, 4-year route cap,
  Graduate visa expiry).
- Report the minimum salary needed on the new-entrant path for the role's
  SOC and hours, against the advert's salary, and record which path
  passed. A salary below £41,700 is never by itself a reason to drop,
  downrank or skip a role.

### Gate 3 — Honest profile fit
Score realistic interview likelihood against his actual profile:
- SAP SuccessFactors: current and UK-based, but transactional/admin level
  — no configuration experience (data model, business rules, workflows,
  MDF, RBP, Integration Center). Score this gap when a role needs
  configuration.
- Workday: a gap.
- Seniority: coordinator level — flag the tension with RQF Level 6 roles.
- Strengths: Python, automation (n8n, Activepieces, Claude API), systems
  thinking, multilingual (English, Hindi, conversational Arabic).
- C_THR81 is scheduled, not held.

### Gate 4 — Employer willingness to sponsor
- **Confirmed:** a statement in the JD, or written confirmation from a
  recruiter or hiring manager.
- **E2 (not evidence):** an ATS question like "do you require
  sponsorship?" — this only shows the question is asked.
- Unknown is a valid answer — say what would confirm it.

### Output
For each role: route, gate-by-gate result with evidence, dual-path salary
result, overall score /5, and apply / don't-apply / need-info verdict.
Keep uncertainty visible.

## 8. Ask the sponsorship question first

Every first-contact outreach template and recruiter-call note includes:
"Can you sponsor a Skilled Worker visa, and could a certificate of
sponsorship be issued by [date]?"

- Tracker columns: `sponsor_confirmed` (confirmed / E2 / unknown / no) and
  `cos_by_date`. Only a JD statement or written recruiter/hiring-manager
  confirmation counts as `confirmed`. An ATS sponsorship question is `E2`
  and does not count.
- After a written "no", close that pipeline row within the same run.

## 9. Warm intro before apply

For every shortlisted role, check `memory/contacts.csv` and
`memory/priority_employers.csv` for a warm path (an existing contact, an
alumnus, a referrer) before the application is prepared. Record
`warm_path` (name or "none") in `memory/tracker.csv`. Contacts are drafted
to, never messaged automatically. No fabricated premises ("as we
discussed", "following my call") unless Fahad has confirmed the call or
conversation happened.

## 10. CV and outreach

CV work follows `rules of cv creation.md`. `/sponsor-sweep` finds roles
only and never drafts a CV.

Outreach guardrails:
- **Draft only.** Save to `outbox/` or Gmail drafts, or show in chat.
  Never call a send, reply or forward tool. Confirm explicitly first, one
  message at a time.
- **Recommend a manual, staggered send** in every outreach batch.
- **No fabricated premises** — see §9.
- **One person, one message.** No near-identical batch text across people
  at the same company.
- **Honest profile** — outreach claims must survive Gate 3.
- **Verify contacts** — say when an address is inferred rather than found.
- **Keep the LinkedIn location UK-facing** in any profile or message copy.
- State how many drafts a batch contains and who they go to, before
  producing it.

## 11. Non-negotiables

1. **Verify, don't recall.** Sponsor licences, SOC codes and salary
   thresholds are checked with tools every time.
2. **Screen on the new-entrant number first** (Gate 2).
3. **Honest fit** — score the configuration gap and seniority tension even
   when it hurts the score.
4. **CVs need a JD.** No job description → stop and ask.
5. **Nothing sends itself.** Fahad approves and sends everything himself.
6. **Plain figures, never "c.".** Write metrics as plain figures on every
   CV, cover letter, application answer and message — never "c.",
   "circa", "around", "approx." or "~" in front of a number.
