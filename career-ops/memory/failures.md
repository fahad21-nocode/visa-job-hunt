# Failures, blocked sources, and scope limitations

Sweep date: 2026-11-17. This consolidates the failure logs from all four discovery passes plus two scope decisions made at the start that depart from a literal reading of the brief — both are flagged here rather than silently absorbed.

## Scope decisions (read these first)

### 1. The register is too large to "resolve every sponsor to its careers board"
The Home Office register, filtered to A-rated Skilled Worker, has **122,918 entities** (saved in full at `memory/register.csv`). Visiting each one's careers page individually is not feasible in one sweep — at any realistic rate that's weeks of continuous crawling, not a session. So the sequencing was flipped: **roles were discovered first** (via job boards, ATS APIs, aggregators, and connectors), and **every role found was then checked against the register** for Gate 1, using the live sponsor-licence lookup tool rather than a static CSV scan (it resolves trading names to legal entities and handles fuzzy matches, which a plain CSV grep can't). This means the sweep is "nothing skipped" at the level of *every role that was found*, but it is not a reverse-crawl of the full register — no claim is made to have checked all 122,918 entities' own job pages.

### 2. Scrapling was not installed; Firecrawl was used instead
The brief asked for `pip install "scrapling[fetchers]"` with specific concurrency/robots/throttle settings. Firecrawl (an already-available MCP tool) was used instead for the same job — concurrent, robots-respecting fetches of ATS JSON APIs and bespoke career pages — since it needed no sandbox setup and gave equivalent coverage. In practice this backfired: **Firecrawl's daily MCP credit allowance ran out early in the session** (confirmed independently by all four parallel discovery agents) and stayed exhausted for the rest of the sweep. This knocked out the planned direct-JSON-API approach to Greenhouse/Lever/Ashby/Workable/SmartRecruiters/Teamtailor/Personio/Recruitee/BambooHR/Pinpoint/Eploy/Oleeo/Jobvite boards almost entirely — no systematic sweep of these ATS APIs was completed. Discovery fell back to WebSearch, direct `curl` against a handful of guessed ATS slugs, `mcp__foundrole__jobs_search`, and the Indeed connector, which is why FoundRole and huntukvisasponsors.com (via search snippets) ended up carrying most of the sweep's volume.

## Domains/sources blocked outright (bot-check, 403, or technical block)

| Domain | Failure mode |
|---|---|
| jobs.nhs.uk (NHS Jobs) | HTTP 403 on search results **and** on individual job-advert URLs (confirmed on retry) |
| civilservicejobs.service.gov.uk (Civil Service Jobs) | "Quick check needed" human-verification screen — not bypassed, per instructions |
| jobs.ac.uk | HTTP 403 on search and on a direct job-advert URL |
| huntukvisasponsors.com | Cloudflare "Just a moment..." challenge (403) on every `/job/` detail page — only reachable via search-engine snippets, which don't carry reliable posting dates |
| totaljobs.com | Connection reset (HTTP/2 stream error); `site:` search filter didn't hold either |
| cwjobs.co.uk | HTTP 403 |
| findajob.dwp.gov.uk | Direct fetch timed out at network layer (WebSearch `site:` queries did work as a workaround — 17 listings used for context) |
| hiring.cafe | HTTP 308 redirect, not followed up |
| welcometothejungle.com | HTTP 403 |
| weworkremotely.com | HTTP 403 |
| applied.com | HTTP 403 |
| workatastartup.com | HTTP 406 |
| joblift.co.uk | HTTP 403 |
| fieldfisher.com/careers | HTTP 403 |
| myvisajobs.com | 200 but fully JS-rendered client-side — no extractable postings from raw HTML |
| studentcircus.com | 200 but pure JS app shell — no extractable postings |
| mhruk.jobs.people-first.com | JS-rendered; one successful Firecrawl scrape (before credits ran out) returned the list but no relevant current vacancy |
| ukvisajobs.com | Its own search route 404'd (site is live — `jobs_count: 18332` visible in embedded JSON — but the query pattern used doesn't match its real client-side-routed search) |
| Firecrawl (firecrawl_search/firecrawl_scrape/firecrawl_map) | Daily MCP credit allowance exhausted session-wide — see scope decision #2 above |

**lgjobs.com and jobsgopublic.com** were not blocked outright but are **unreliable**: both returned HTTP 200 every time, but the keyword/query parameter was never applied server-side — every attempt (multiple param-name variants, both sites) returned the same unfiltered default listing (~9,052 and ~10,834 jobs respectively, almost entirely unrelated roles). No results from either site could be trusted as keyword-matched, so none were added to the tracker.

**relocate.me** loaded fine but is scoped to developer/tech relocation roles only (Android, Java, DevOps, Python, etc.) — zero relevant categories for this candidate's role families; a scope mismatch, not a block.

## Sources skipped per instructions (no connector, scraping forbidden)

**LinkedIn, Glassdoor, ZipRecruiter** — no approved connector exists for any of these; not scraped, per the brief.

## The one source that reliably worked

**Indeed**, via the `mcp__Indeed__search_jobs` / `get_job_details` connector tools, was the only government/public-sector-adjacent-reachable source that returned consistent, dated, keyword-matched results across all 11 role families. It has no native "posted within 14 days" filter, so recency was enforced manually against each result's own posted date.

## Sponsors found in discovery with no clean Gate 1 match

- **Quince** (US DTC retailer) — only register hit is an unrelated landscaping company; no UK licence found.
- **SANS Institute** — no UK or NL register match under that name.
- **Jobgether** — a job-board intermediary; the real hiring employer was never disclosed in the posting, so Gate 1 couldn't be resolved at all.
- **UBDS Group Limited** — not found under that exact name; found instead as "UBDS IT Consulting Ltd" (A-rated, confirmed) — a naming mismatch, not a missing licence.
- **OpenView** (recruiter/trading name advertising a Payroll & HR Officer role) — the real hiring entity was never named in the advert; also carries a 4-years'-UK-residency / "work authorisation: UK required" line, a strong signal of no sponsorship. Marked out on Gate 4, not pursued further on Gate 1.
- **ABM Industries Inc.** — not found under that name; the JD's own "ABM UK" reference fuzzy-matched ABM Aviation UK Limited (0.861) — plausible given the Heathrow/Hounslow location, but marked **unconfirmed**, not failed, per Gate 1 rules.
- **Enfield Council** — no plausible A-rated match (consistent with many local-authority bodies sitting outside the Skilled Worker register); moot anyway, as the role was a Level 4 apprenticeship.
- **Visa Europe Services LLC** — only a low-confidence (0.638) fuzzy match to "Visa Europe Limited"; marked unconfirmed. Moot anyway — SOC 4143 isn't currently sponsorable for a new CoS.
- **Volaris Group UK Holdco Ltd / ClickDimensions** — the parent holdco is A-rated and licensed, but "ClickDimensions" (the advertised hiring brand) has no separately-listed UK entity. Marked **unconfirmed**, included in the shortlist on that basis (see `shortlist.md` #6).

## Sponsors found with no findable careers board at all (guessed ATS slugs 404'd)

Thought Machine, Sportradar, Smart Pension, Version 1 / Version1Consulting, Linnworks, MHR Global, Kainos, ICS.AI, Robiquity, Tomoro, Haymarket, Saffery, Fieldfisher, Murphy Group, DAC Beachcroft, VVB Engineering, Deputy (UK-relevant postings not actually based in the UK), Board Intelligence (connection timeout). **DoubleVerify's** Greenhouse board resolved correctly but had zero open roles at all. This list reflects slug-guessing only (since the Firecrawl-driven systematic ATS sweep didn't run) — it is not proof these employers have no board, only that a guessed Greenhouse/Lever slug didn't resolve.

## Retry pass

A full automated retry (resuming each of the four discovery agents after they separately hit a session-wide 5-hour API rate limit) re-ran failed/empty sources with the same methods — results unchanged on every site listed above as "blocked." A supplementary manual retry (WebSearch, broader keywords, targeting revenue/CRM operations, automation/RPA, and talent/recruitment operations specifically, plus a `site:ukvisajobs.com` attempt) surfaced ~77 additional candidate listings, but on inspection every one was either: outside the 14-day posting window (most were from February–September 2026), an explicit no-sponsorship role (B.Braun CRM Administrator, YU Energy Junior Automation Developer, Multiverse Talent Operations Coordinator, Creative Support Recruitment Coordinator), already closed, or a duplicate of a role already screened by one of the four agents. The `site:ukvisajobs.com` filter did not hold — Google indexed huntukvisasponsors.com results instead. No new rows were added to the tracker from this pass; it's logged here to show it was tried, not skipped.
