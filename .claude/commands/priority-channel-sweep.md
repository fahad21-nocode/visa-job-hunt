---
description: Sweep the consultancy/outsourcer priority channel on the employers' OWN careers portals (not aggregators), run the four-gate screen on every hit and on general-sweep HRIS finds, and log results. Finds and screens only. No CVs, nothing sent.
argument-hint: "[optional: brand name(s) to limit the run, or 'dry-run']"
---

# /priority-channel-sweep

You are working in Fahad's career-ops workspace. This command follows on from `/strategy-reset`. The last run searched FoundRole and Indeed for the priority-channel keywords, found zero roles at the 14 cleared consultancy/outsourcer brands, and logged that as "a real signal" in `memory/intel.md`. That conclusion is wrong. Both are job aggregators, and large consultancies and outsourcers mostly hire through their own careers portals (Workday, SuccessFactors, Taleo, Phenom, Eightfold, Avature and similar) and through graduate or associate intakes, which aggregators index poorly. This command fixes the log and sweeps the right sources.

If `$ARGUMENTS` names brands, limit the run to those. If it contains `dry-run`, plan and print the source list per brand without fetching any job data.

## Hard rules

- Use the Scrapling skill for the sweep: `npx skills use "https://github.com/d4vinci/scrapling" --skill "scrapling-official"`. Keep `robots_txt_obey` on. Prefer an ATS JSON endpoint wherever the portal exposes one, use `page.markdown()` for JD text, and `capture_xhr` for portals that load jobs by XHR.
- Resource limits: HTTP concurrency 4, at most 2 browser sessions, and never run browser fetchers alongside a 14B local model.
- Don't scrape LinkedIn, Indeed, ZipRecruiter, Dice or Glassdoor. Use their official connectors if needed.
- Scope is UK-wide (any UK location, hybrid or remote), not London-only.
- This command finds and screens only. Don't draft CVs or cover letters. Don't submit applications. Don't send, reply to or forward any message. Outreach questions are written to `outbox/` as drafts for Fahad to send himself, manually and staggered.
- Never assert a SOC code, going rate or sponsor licence from memory. Verify at run time with the sponsor register tools, `check_salary_threshold` and gov.uk.
- Write his figures as plain numbers. No "c.", "circa", "around", "approx." or "~".
- Respect the tooling freeze: don't install new tools other than the Scrapling skill above.

## Step 1: Correct the intel log

In `memory/intel.md`, find the entry claiming that zero FoundRole and Indeed results for the 14 brands is a real signal. Don't delete it. Append a dated correction:

> Correction (/priority-channel-sweep, <date>): FoundRole and Indeed are both aggregators, so agreement between them isn't independent evidence. Consultancies post mainly on their own portals and graduate/associate programmes. The channel is untested until their own careers sites are swept. Result of that sweep: <fill in at Step 6>.

## Step 2: Resolve each brand's own careers portal

For each brand in `memory/priority_employers.csv` (seed list if missing: Infosys, Tata Consultancy Services, Wipro, HCLTech, Cognizant, Capgemini, NTT DATA, Tech Mahindra, LTIMindtree, Accenture, IBM, Deloitte, PwC, KPMG, EY):
- Find the official careers site from the company's own domain. Don't take it from a third-party listing. Record `careers_url`, the ATS platform behind it, and the JSON endpoint if there is one.
- Also record any UK graduate, associate, early-careers or lateral-hire programme pages (these often sit outside the main job search).
- Fill or refresh the Gate 1 columns (`legal_entity, register_match, rating, route, verified_on`). Resolve the UK hiring entity's legal name first, then use both `check_sponsor_license` and `search_sponsors`, and compare name, Companies House number and location. Reject fuzzy matches under 5 characters. A parent's licence doesn't cover a subsidiary unless it's linked, so if only the parent is listed, mark it **unconfirmed**, not failed.
- If a portal blocks automated access or robots disallows it, mark `manual_check_needed` with the URL and move on. Don't try to get around the block.

## Step 3: Sweep the portals

Filter to UK locations and these priority keywords: SuccessFactors (support, AMS, Employee Central, functional consultant), HRIS support, HR systems analyst, HR operations analyst, people systems, application support analyst, service desk analyst, business systems analyst, associate/graduate consultant (HR technology, SAP, ERP, HCM), workforce/HR data analyst.
- Dedupe against `memory/seen.jsonl` and add new job IDs to it.
- Skip 12-month fixed-term contracts.
- Save each new role to `memory/tracker.csv` with `channel=consultancy`, the source URL, the posted date and the full JD text (as markdown in `memory/jds/<id>.md`).

## Step 4: Add the general-sweep HRIS finds

Add these from the last run to the tracker with `channel=in-house`, if they aren't there already: GXO Logistics (Senior HR Systems Analyst), Motability Operations Ltd (HRIS Analyst), Bernard Matthews (HR Systems and Data Analyst), ABM Industries (HR Systems Analyst), Withersworldwide (HRIS Analyst, 9-month contract), ERP Tech Solutions Ltd (SAP SuccessFactors Lead), Quanex (Senior ERP Support Analyst).

Record the two already screened in chat on 12 Nov 2026:
- **GXO Logistics UK Limited: don't apply.** Gate 1 pass (A-rated, Skilled Worker, exact match). Gate 2 pass (up to £64,800, 40 hours). Gate 3 fail: needs a SuccessFactors Recruiting/Onboarding 2.0 configuration expert who has led multiple implementations and done Integration Center work. Score about 2/5.
- **Motability Operations Ltd: need info.** Gate 1 pass (A-rated, Skilled Worker, exact match). Gate 2 open because the advert has no salary or hours. If coded SOC 2133, the new-entrant minimum is £38,400 at 37.5 hours (checker verified 12 Nov 2026). If coded SOC 3549 as a business systems analyst on the TSL, the floor is £33,400, but the CoS must be issued before 31 Dec 2026. Gate 3 is decent. HAVE: workflow automation (n8n, Activepieces, Power Apps/Copilot Studio at TfL), testing, documentation, change control, Git, case handling, adoption support. GAP: HRIS configuration, a dashboard build he can evidence, ResourceLink/Eploy. Gate 4 unknown. Score about 3.6/5.

## Step 5: Four-gate screen for every new role

For each role from Steps 3–4 not yet screened, run all four gates exactly as `career-ops-rules.md` defines them:
- **Gate 1:** as in Step 2.
- **Gate 2:** map the actual duties to a SOC 2020 code and say why. Run `check_salary_threshold` with the real weekly hours, new-entrant path first, then the general path (£41,700 or the going rate, whichever is higher), then ISL/TSL. Check the code and title the checker mapped to, since it mis-maps titles. Retry with a closer title or the code itself, and label anything you can't settle "not tool-verified". If salary is missing, report the minimum needed on the new-entrant path. A salary under £41,700 is never by itself a reason to drop a role.
- **Gate 3:** score honestly against his real profile. SuccessFactors at transactional level (no data model, business rules, workflows, MDF, RBP or Integration Center). Workday gap. Coordinator-level seniority, so flag the tension with RQF 6. Power BI intermediate, with no evidenced dashboard or data modelling. No C_THR81 (exam cancelled).
- **Gate 4:** only a JD statement or written recruiter/hiring-manager confirmation counts as confirmed. An ATS "do you require sponsorship?" question is E2.
- **TSL tag:** if the role sits in an RQF 3–5 occupation that is on the current interim TSL/ISL (verify on gov.uk), tag it `TSL-WINDOW` with days left to 31 Dec 2026. Apply gate: 3.5/5 for these, 4.0/5 for RQF 6+.
- **Verdict:** apply / don't-apply / need-info, with the evidence used.

## Step 6: Outbox drafts (draft only)

For each `need-info` role scoring 3.5 or above, write one draft to `outbox/questions/<employer>-<role>.md`, starting with Motability. Keep it short and tailored to that employer. Ask for the salary and weekly hours, and whether they can sponsor a Skilled Worker visa with a certificate of sponsorship issued by [date]. No fabricated premises, and no claims that fail Gate 3. Add `warm_path` from `memory/contacts.csv` if one exists. Don't send anything.

Then complete the correction in `memory/intel.md` with the real result of the portal sweep.

## Step 7: Report

Write `memory/runs/priority-channel-sweep-<YYYYMMDD-HHMM>.md` and print:
1. A brand table: portal found (Y/N), ATS, Gate 1 status, UK roles found, `manual_check_needed`
2. Ranked shortlist: role, employer, channel, route, Gate 1–4 results, new-entrant minimum vs advertised salary, score, verdict, `TSL-WINDOW` days
3. Drafts written to `outbox/` (count and recipients). Remind Fahad to send manually and staggered.
4. Advance-rate note per channel and role family, if there is tracker history
5. Anything blocked and why
