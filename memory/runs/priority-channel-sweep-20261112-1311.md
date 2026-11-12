# /priority-channel-sweep run report — 2026-11-12 13:11 UTC

## Context

This run corrected a mistake from the previous `/sponsor-sweep` run: zero
priority-channel results on FoundRole and Indeed was logged as "a real
signal" that the consultancy/outsourcer channel was weak. Both are
aggregators, so their agreement wasn't independent evidence — see the
correction in `memory/intel.md`. This run swept the 15 priority
employers' own careers portals instead, then four-gate-screened every
new find plus the 7 general-sweep candidates from the prior run.

It also caught and refused a fabricated claim in the command text that
two roles (GXO Logistics, Motability) had already been screened in a
prior chat with specific figures — that screening never happened, so
both were screened for real instead. See `memory/intel.md` for the full
note.

**Sourcing note:** `career-ops-rules.md` specifies the Scrapling skill.
It installed cleanly but this sandbox's network proxy blocks direct HTTP
to company domains outright (allowlist-only), which is a sandbox
constraint, not a robots.txt/anti-bot block. Substituted Firecrawl's MCP
tools for this run — see `memory/decisions.md`.

## 1. Brand table

| Brand | Portal found | ATS | Gate 1 | UK roles found | manual_check_needed |
|---|---|---|---|---|---|
| Infosys | Y | iCIMS/jobs2web | PASS (A) | 0 | No — UK list checked, ruled out |
| Tata Consultancy Services | Y | iBegin (proprietary) | PASS (A) | 0 | **Y** — portal identified, not keyword-searched (time budget) |
| Wipro | Y | SuccessFactors/jobs2web | PASS (A) | 0 | **Y** — SF roles exist on portal, UK location unconfirmed (locale tags unreliable) |
| HCLTech | Y | SuccessFactors/jobs2web | PASS (A) | 0 | **Y** — 169 UK roles, not fully paginated |
| Cognizant | Y | proprietary (Avature-style) | PASS (A) | 0 | **Y** — "UK&Ireland" URL actually serves an unfiltered global feed |
| Capgemini | Y | proprietary | PASS (A) | **3** | No |
| NTT DATA | Y | proprietary | PASS (A) | 1 | No |
| Tech Mahindra | Y | proprietary | PASS (A) | 0 | **Y** — live vacancy portal not keyword-searched directly |
| LTIMindtree | Y (rebranded "LTM") | proprietary | **REMOVED from register 2026-09-01** | 0 | **Y** — also re-check Gate 1 under "LTM" if the legal entity changed with the rebrand |
| Accenture | Y | Workday + Pinpoint | PASS (A) | **2** | No |
| IBM | Y | proprietary | PASS (A) | 0 | **Y** — only global multi-locale postings found, no confirmed UK locale |
| Deloitte | Y | Avature | PASS (A) | **1** | No |
| PwC | Y | Phenom | PASS (A) | 2 | No (JDs not fetched — JS-rendered) |
| KPMG | Y | proprietary | PASS (A) | 2 (1 excluded, 12-month FTC) | No |
| EY | Y | SuccessFactors/jobs2web | PASS (A) | 0 | **Y** — only non-UK SF postings found |

**11 new roles** logged to `memory/tracker.csv` this run (3 Capgemini, 2
Accenture, 1 Deloitte, 2 PwC, 1 KPMG screened + 1 KPMG excluded, 1 NTT
DATA), all now four-gate-screened. 7 brands still need a proper
keyword-filtered pass on their own portal (TCS, Wipro, HCLTech,
Cognizant, Tech Mahindra, IBM, EY) before anything can be concluded about
them specifically — "0 found" there reflects an incomplete search, not a
confirmed absence of roles.

## 2. Ranked shortlist

### Need-info (worth a drafted question)

| Role | Employer | Channel | Route | Gate 1 | Gate 2 | Gate 3 | Gate 4 | Score | TSL-WINDOW |
|---|---|---|---|---|---|---|---|---|---|
| HR Systems and Data Analyst | Bernard Matthews | in-house | R1 | PASS | Plausible pass (SOC uncertain) | Good — SF is desirable not essential | Unknown | 3.7 | Tentative, 49 days |
| HRIS Analyst | Motability Operations Ltd | in-house | R1 | PASS | Open (no salary stated) | Partial — Power Automate not a confirmed HAVE | Unknown | 3.5 | Possible, unconfirmed SOC |
| AV Support Engineer | Wipro | consultancy | R1 | PASS | Not run | Unclear — thin posting, no stated requirements | Unknown | 2.0 | No |

### Don't-apply (sponsor confirmed, fails on fit — ranked by score)

| Role | Employer | Score | Why |
|---|---|---|---|
| HR Systems Analyst | ABM Industries | 2.3 | Gate 1 only a plausible match (not exact); Oracle Fusion HCM platform mismatch |
| GXO Logistics SF role | GXO Logistics | 1.8 | SF Recruiting/Onboarding configuration-expert requirement |
| Workday Absence Time Tracking Lead | Accenture | 1.5 | Workday gap, consulting-lead level |
| MS Dynamics365/Power Platform Support Analyst | NTT DATA | 1.5 | C#/JavaScript/Dynamics 365 CE — platform/language gap, not HR-tech |
| HR Transformation Senior Consultant | Capgemini | 1.3 | Senior consultant, SF Practice (title-scored) |
| SF EC & Time Mgmt Associate Manager | Accenture | 1.3 | SF EC certifications required, full-lifecycle implementation experience |
| HRIS Analyst (9-month contract) | Withersworldwide | 1.3 | Deep SF config + expert Power BI required |
| SAP SuccessFactors Lead – HR Technology Manager | ERP Tech Solutions Ltd | 1.3 | People-manager role, SF config leadership |
| 9 further roles (HCLTech ×2, Capgemini ×2, Accenture SME, Deloitte Manager, PwC ×2, KPMG Principal Architect, Quanex/Liniar, NTT Global Data Centers) | various | 1.0 | Decisive seniority (Lead/Architect/Manager/SME/Principal) or domain mismatch (robotics, SAP Business One, Workday) — full detail in tracker.csv |

**Pattern worth flagging on its own:** every one of the 10 dedicated
SuccessFactors roles found this run — on aggregators and on the
employers' own portals alike — required either certified hands-on SF
configuration experience or sat at Senior Consultant/Manager/Architect
level and above. None were at coordinator/analyst, non-configuration
level. That's a real, now twice-confirmed signal about the ceiling on
*dedicated SF roles* specifically at these 15 brands — not about the
channel's discoverability, which was the earlier (wrong) conclusion.

## 3. Outbox drafts

2 drafts written to `outbox/questions/`, both cold outreach (no warm path
on file in `memory/contacts.csv`):
- `motability-operations-ltd-hris-analyst.md`
- `bernard-matthews-hr-systems-and-data-analyst.md`

**Nothing has been sent.** Fahad sends each one manually, staggered —
not both at once.

## 4. Advance rate

No applications have been submitted yet this run (weekly cap untouched —
0/10), so there's no advance-rate data to report. Channel/role-family
split of what's been screened so far: consultancy channel 16 roles
screened (0 apply, 0 need-info, 16 don't-apply), in-house 7 roles screened
(2 need-info, 5 don't-apply). All in the HR systems/HRIS and business
systems & application support role families — no R3/R4 or other role
families swept yet.

## 5. Blocked / open items

- Scrapling unavailable in this sandbox (network proxy allowlist) —
  substituted Firecrawl; see `memory/decisions.md`.
- 7 brands' own portals (TCS, Wipro, HCLTech, Cognizant, Tech Mahindra,
  IBM, EY) need a proper keyword-filtered pass — `manual_check_needed` in
  `priority_employers.csv`.
- LTIMindtree's register status should be re-checked under "LTM" in case
  the legal entity changed with the rebrand.
- ABM Industries' Gate 1 match ("ABM Services Limited") is plausible by
  location only, not a confirmed legal-entity match — needs a Companies
  House check against ABM's actual UK corporate structure.
- Capgemini's Senior SAP SuccessFactors EC Payroll Consultant role
  requires SC clearance (5 continuous years' UK residency) — flagging in
  case this comes up again on a similar role; residency history wasn't
  checked against this requirement.
- Accenture's Associate Manager posting has a closing date (31/08/2026)
  already in the past — likely stale, not re-verified live.
