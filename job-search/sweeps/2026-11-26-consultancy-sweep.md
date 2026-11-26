# Consultancy sweep, 26 Nov 2026 (first pass, incomplete)

Result: 0 roles pass the apply gate today. 0 roles go to the weekly top 10-15. No hiring-manager lookups were run, so no Hunter or Monid credits were spent.

## Coverage
| Employer | Status |
|---|---|
| Accenture | Swept via FoundRole (3 queries). 3 roles found. |
| Infosys | Swept via FoundRole. 2 roles found. |
| Cognizant | Swept via Indeed. 4 roles found. |
| TCS, Wipro, HCLTech, Capgemini, NTT DATA | Not covered. FoundRole returned nothing for these in 30 days for Business Analyst and Data Analyst. Indeed returned nothing for Capgemini and Infosys, and was rate-limited for NTT DATA. |
| Big 4 managed services | One FoundRole HRIS query across EY, Deloitte, PwC, KPMG and the consultancies returned 0. Not otherwise swept. |
| Temporary Shortage List | No role was checked against the TSL. No TSL roles surfaced. Needs a check against the current gov.uk list. |

Why it is incomplete: Firecrawl credits ran out, Indeed rate-limited the account, and FoundRole's visa signals are US H-1B data, so they are not used as UK evidence.

## Temporary Shortage List check (gov.uk, read 26 Nov 2026)
- Sources: MAC "Temporary Shortage List: Stage 2 report" and the interim TSL in Appendix Skilled Worker (SW 6.1A). Both the expanded Immigration Salary List and the interim TSL expire on 31 Dec 2026.
- The MAC recommends 28 occupations for 18-month TSL access (none for the full three years). These are mostly construction trades, clean energy, foundational industries and three digital roles.
- The three digital occupations are 3133 Database administrators and web content technicians, 3544 Data analysts, and 5242 Telecoms and related network installers and repairers.
- Only 3544 Data analysts matches your role families, so data-analyst roles are the TSL priority. HRIS, HR operations, business systems support, service operations and project roles are not on this list as far as I read, so they need RQF 6+ and the 4.0 gate.
- The report says TSL jobs do not get a discounted salary unless they are also on the Immigration Salary List. The new-entrant path (70% of the going rate, minimum £33,400) still needs checking per role with the checker or gov.uk. Entering 3544 directly in the checker has failed before.
- I read the Stage 2 recommendation, not the final published list. Before scoring any role as TSL, confirm that code is in force in SW 6.1A/6.1B in the current rules.

## Roles found and screened
Salary is shown only where the advert or a FoundRole estimate gave one. No advert stated a salary, so Gate 2 is "need-info" for all of them. Estimates are not adverts.

| # | Employer, role, location | Posted | Gate result | Verdict |
|---|---|---|---|---|
| 1 | Accenture, Business Analyst, Newcastle (hybrid) | 30 Oct | Requires BPSS and SC clearance, which needs 5 years' continuous UK address history. Likely blocks on the Graduate-visa timeline. Estimate median £42,730. | Don't apply, unless Fahad confirms he meets the 5-year rule |
| 2 | Accenture, Senior Business Analyst (Technical), Newcastle | 30 Oct | Same clearance requirement plus senior-level coaching and leadership asks. | Don't apply |
| 3 | Accenture, Analytics & Data Insight Consultant, London | 4 Nov | Alteryx, Tableau or Power BI is essential and ideally certified. Power BI is intermediate with no evidenced dashboard, and he holds no certification. Estimate median £36,500. | Don't apply, fit below gate |
| 4 | Infosys, Senior Consultant Data Business Analyst, London | 28 Oct | Needs insurance and reinsurance domain knowledge, Snowflake, source-to-target mapping. Seniority tension. | Don't apply |
| 5 | Infosys, Associate Business Analyst (Cyber), London | 25 Nov | Cyber monitoring work, outside his profile. | Don't apply |
| 6 | Cognizant, Project & Triage Associate, Remote | 19 Nov | Plausible fit for service operations. Cognizant Worldwide Limited is on the register (A rating, Skilled Worker, London). Not confirmed that this entity hires for the role. Job description not read (Indeed rate-limited). | Need-info: re-run job details, check salary and SOC code |
| 7 | Cognizant, Workday Integrations Consultant, Remote | 26 Oct | Workday is a gap, integration configuration needed. | Don't apply |
| 8 | Cognizant, AI SDLC Solution & Enablement Lead, London | 25 Nov | Lead-level. | Don't apply |
| 9 | Cognizant, Non-Functional Test Assurance Engineer, London | 25 Nov | Testing specialism. | Don't apply |

### Second pass (FoundRole, Application Support Analyst and Data Analyst, last 45 days)
| # | Employer, role, location | Posted | Gate result | Verdict |
|---|---|---|---|---|
| 10 | Infosys, Technology Analyst, Sales & Trading EUC/DSS Support, London (Canary Wharf, 5 days on site, weekend overtime) | 24 Nov | Level 2/3 desktop and end-user support. Estimate median £28,250, likely under the £33,400 new-entrant floor. Not TSL. | Don't apply |
| 11 | HCLTech, Support Engineer (Robotics Teleoperator), London | 23 Nov | Physical VR/robot data-collection role. | Don't apply |
| 12 | HCLTech, Senior Technical Specialist (Java/blockchain), London | 17 Nov | 5+ years engineering. | Don't apply |
| 13 | HCLTech, Senior Technical Specialist (GCP DevOps), London | 20 Nov | Cloud/Terraform/Kubernetes, not his profile. | Don't apply |

Not seen: the application-support search reported 5 more results hidden behind FoundRole's preview limit, and the Data Analyst search across Deloitte, PwC, EY, KPMG, Capgemini, NTT DATA, TCS, Wipro and HCLTech reported 1 hidden result and showed none. Those need the FoundRole site or each employer's own board.

## Sponsor register checks (data as of 24 Nov 2026)
- Cognizant Worldwide Limited: A rating, Skilled Worker and Global Business Mobility routes, London. Exact name match to the register entry.
- Dataiku Ltd: A rating, Skilled Worker route, London. Used for the warm-contact draft.
- A parent or sister company licence does not cover a hiring entity unless that entity is linked, so role 6 stays unconfirmed until the employer says so.

## Next sweep steps
1. Retry Indeed job details for the Cognizant triage role, then run `check_salary_threshold` once the salary and hours are known.
2. Sweep TCS, Wipro, HCLTech, Capgemini and NTT DATA through their own career boards or the browser, not paid scrapers.
3. Check RQF 3-5 roles against the current gov.uk Temporary Shortage List before scoring.
4. Add Big 4 managed-services roles (EY, Deloitte, PwC, KPMG) by direct search.
