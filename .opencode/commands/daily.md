# daily

The OpenCode/OpenWork agent's daily/weekly career-ops sweep. Read
`AGENTS.md` and `career-ops-rules.md` before running this. On any
disagreement between this file and `career-ops-rules.md`, the rules file
wins — flag it, don't silently follow this file.

## Hard constraints for this command

- Never submit an application or send a message. `auto_apply` and
  `auto_send` are `false` in `opencode.json`. This command only prepares
  drafts into `outbox/` and updates `memory/`.
- Weekly cap: 10 fully tailored applications (`opencode.json
  .agent.weekly_application_cap`). Once the week's count in
  `memory/applications.csv` hits the cap, every further qualifying role
  this run goes to `memory/backlog.csv`, ranked by score — not dropped,
  not applied to.
- Tooling freeze is in force until 17 Feb 2027 (`career-ops-rules.md`
  §0). Don't add a scraper, board or MCP server to make this run easier
  without asking first.
- Never assert a SOC code, going rate or sponsor licence from memory —
  verify with the sponsor-register tools / `check_salary_threshold` /
  gov.uk every time.

## Run order

### 1. Priority employers first
Sweep `memory/priority_employers.csv`. For every row missing
`legal_entity`..`verified_on`, resolve the legal entity and run Gate 1
(`career-ops-rules.md` §7) now, writing the result back into the row.
Search this channel's priority keywords (SuccessFactors support/AMS,
HRIS support, HR operations analyst, application support analyst,
service desk analyst, graduate/associate consultant (HR tech/SAP/ERP),
people systems) against each verified employer's careers page/ATS.

### 2. TSL-window tagging
For every RQF 3–5 role found (this run or already in `memory/tracker.csv`
and unresolved), verify at run time whether the occupation is on the
current TSL/ISL and whether the employer can plausibly issue a CoS by
mid-December 2026 (`career-ops-rules.md` §4). Tag qualifying roles
`TSL-WINDOW`, surface them first in output, and show the countdown in
days to 31 December 2026.

### 3. General sweep
Run the register-first sweep across all eleven role families
(`career-ops-rules.md` §2), R1 and R2.

### 4. R3 and R4 — parallel tracks
Run R3 (remote for an India base, or in-office India GCC HR-tech /
founding-stage AI startup roles) and R4 (Gulf) as their own sections,
every run, not only when R1 is thin.

### 5. Per role, before preparing anything
- Score against the four gates and the apply gate (3.5/5 for RQF 3–5
  until 31 Dec 2026, else 4.0/5).
- Check `memory/contacts.csv` and `memory/priority_employers.csv` for a
  warm path; record it in `tracker.csv.warm_path` ("none" if there isn't
  one).
- If outreach is drafted, open with the sponsorship question
  (`career-ops-rules.md` §8) and record `sponsor_confirmed` / `cos_by_date`.
  Close the row in the same run on a written "no".
- Prepare the application/draft into `outbox/` only if under the weekly
  cap; otherwise append to `memory/backlog.csv`.

## Output

- Advance rate per channel (`consultancy` / `in-house` / `agency` /
  `public sector`) and per role family.
- A section each for R1, R3, R4 (R2 folded into the general sweep
  output).
- `TSL-WINDOW` roles listed first, with the days-remaining countdown.
- Weekly cap status: applications prepared this run vs the cap, and what
  went to `memory/backlog.csv`.

## On 1 January 2027

Revert the RQF 3–5 apply gate from 3.5/5 to 4.0/5 without being asked,
and log the change (date, old value, new value) in `memory/decisions.md`.
