# Failures and blocked/skipped sources log — discovery run 4 (2026-11-17)

## A. NHS Jobs (jobs.nhs.uk) — BLOCKED
- Direct fetch of the search-results URL (`/candidate/search/results?keyword=...`) via WebFetch
  returned **HTTP 403 Forbidden** on first live test (keyword "HRIS").
- Retried via `mcp__Firecrawl__firecrawl_scrape` on the same URL: the Firecrawl connector was out of
  daily MCP credits (not a site-level verdict either way).
- Per instructions, logged as blocked and not bypassed. All 13 required keywords ("HR systems",
  "HRIS", "business analyst", "systems administrator", "data analyst", "application support",
  "business support", "project coordinator", "PMO", "recruitment coordinator", "CRM administrator",
  "customer service", "automation") are logged in sources_4.csv as attempted/blocked rather than
  re-sent individually against a confirmed site-level block.
- **No NHS Jobs roles could be screened this run.**

## B. Civil Service Jobs (civilservicejobs.service.gov.uk) — BLOCKED
- Direct fetch of the search URL returned a **"Quick check needed" human-verification screen**
  (tick-box + Continue) instead of job listings, on first live test (keyword "business analyst").
  This is the bot-check the task explicitly says to log and move past, not solve.
- All 13 required keywords logged in sources_4.csv as attempted/blocked.
- **No Civil Service Jobs roles could be screened this run.**

## C. jobs.ac.uk — BLOCKED
- Direct fetch returned **HTTP 403 Forbidden** on two different search-URL query formats tested
  (keyword "business analyst").
- All 13 required keywords logged in sources_4.csv as attempted/blocked.
- **No jobs.ac.uk roles could be screened this run.**

## D. lgjobs.com and jobsgopublic.com — UNRELIABLE (search filter not applied)
- Both sites returned a 200 page each time, but the keyword/query-string parameter was **not
  applied server-side** — every attempt (two query-param name variants per site, both tested on
  "business analyst") returned the identical unfiltered default job listing (lgjobs.com: ~9,052
  jobs; jobsgopublic.com: ~10,834 jobs), almost entirely unrelated roles (forestry operatives,
  planning officers, police constables, etc.). A third guessed search path on jobsgopublic.com
  404'd. These sites appear to require a JS-rendered front-end search that a plain HTTPS GET
  cannot drive.
- Because results could not be reliably matched to any keyword, **no lgjobs.com or jobsgopublic.com
  roles are included in discovery_4.csv** (including no false "zero results" — the handful of
  jobs visible, e.g. a "Business Analyst - Fixed Term" at Cambridge City Council, were surfaced by
  chance on the default listing, not by a working search, and that particular role is also a
  fixed-term contract under 12 months and so OUT regardless).
- All 13 required keywords logged in sources_4.csv per site as attempted/unreliable.

## E. Firecrawl (used as a fallback fetch tool) — OUT OF CREDITS
- `mcp__Firecrawl__firecrawl_scrape` returned "Insufficient credits for this connected-app
  request" on every attempt this run (NHS Jobs, Civil Service Jobs). The tool's own guidance said
  not to retry with different parameters. Did not retry further.
- Your Firecrawl credits ran out. Daily MCP credits refresh in 8m (at the time of first failure).
  Add credits or upgrade to keep going: https://www.firecrawl.dev/billing/s/XYPgx5FU2s3MznxIgyE6gw5-u82SK3Srp-3nyKArjv8

## F. LinkedIn, Glassdoor, ZipRecruiter — SKIPPED (no connector, per instructions)
- Not attempted. No approved connector exists for these sites and the brief explicitly forbids
  scraping them directly.

## G. Indeed (mcp__Indeed__search_jobs / get_job_details) — WORKED
- This was the only source that returned usable, keyword-matched, dated results this run. All 11
  role families were searched (location=London, country=GB) and the most relevant/recent hits had
  full job details pulled and were screened through all 4 gates — see discovery_4.csv.
- Note: the connector has no native "posted in last 14 days" filter, so recency was enforced
  manually against each result's "Posted on" date (today = 2026-11-17, cutoff = 2026-11-03).
  Many returned results were older than 14 days and were excluded from screening (logged in
  sources_4.csv row counts as returned, but only the in-window ones were screened).

## Sponsors checked with no clear match found on the register
- **OpenView** (advertiser for "Payroll and HR Officer", Rickmansworth) — `not_found` on the
  sponsor register. The advert is from a recruiter/trading name; the actual hiring entity (a
  "market leader in Tech/Electronics") is not named in the posting, so Gate 1 cannot be resolved.
  The advert also requires 4 years' UK residency and "Work authorisation: United Kingdom
  (required)" — a strong signal this role is not being sponsored. Verdict: out.
- **ABM Industries Inc.** (as literally named by Indeed) — `not_found`. The JD itself says "ABM UK",
  which fuzzy-matched to **ABM AVIATION UK LIMITED** (A-rated, Skilled Worker, Hounslow) at 0.861
  confidence — plausible given the job's Heathrow/Hounslow location, but not a certain match to
  the exact legal entity that would issue a CoS. Flagged "unconfirmed" rather than failed, per Gate
  1 rules.
- **Enfield Council** (end-client for the AI & Automation Apprentice role, via Apprentify) —
  `ambiguous`, no plausible match on the A-rated Skilled Worker register (consistent with the
  known fact that many public-sector/local-authority bodies are not on it). Moot anyway: this is a
  Level 4 apprenticeship, not normally sponsorable under Skilled Worker, and likely pays well below
  the salary floor.
- **Visa Europe Services LLC** — `ambiguous` (best match "Visa Europe Limited" at 0.638, below a
  safe-confidence bar). Not relied upon; Gate 1 marked unconfirmed. Moot anyway: the role's SOC
  (customer service managers, 4143) is currently sponsorable only for workers already sponsored in
  it pre-22 Jul 2025, so a new CoS is not available regardless of entity.
