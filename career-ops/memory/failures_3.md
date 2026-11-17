# Source failures log (discovery_3)

- Firecrawl (search/scrape/map): insufficient credits at start of session (daily MCP allowance exhausted). Retried after ~8 min wait window with a trivial test query; still out of credits. Not retried further. Fell back to WebSearch, mcp__foundrole__jobs_search, and the sponsorship MCP tools for the rest of the run. This means no Greenhouse/Lever/Ashby/Workable/etc. JSON API endpoints were queried directly in this run (the plan called for curl/Firecrawl against boards-api.greenhouse.io, api.lever.co, etc. - none of this was attempted because the tool meant to drive it was unavailable and raw curl against unknown employer slugs without a discovery step was judged too low-yield to prioritise with the remaining budget).

- foundrole.com (job detail pages): WebFetch returned HTTP 404 on 3 direct job-detail URLs (foundrole.com/job/...). The site appears to render an account-marker token client-side that a plain fetch doesn't carry. Not a blocker in practice - mcp__foundrole__jobs_search already returned full job description text inline for every result, so the job-detail fetch wasn't needed.

- huntukvisasponsors.com (job detail pages): WebFetch returned HTTP 403 Forbidden on every direct job-detail URL tried (5 attempts: Laing O'Rourke PMO Control Room Coordinator, SmartCo Consulting Snr PMO Analyst, CameraMatics Head of Revenue Operations, Yondr Group Talent Acquisition Specialist, Forsyth Barnes CRM Operations Manager). The site blocks non-browser fetches. Could only see these via WebSearch result snippets, which don't give reliable posting/closing dates - all 5 were dropped from discovery_3.csv rather than included with unverified dates.

- Indeed, LinkedIn, Glassdoor, ZipRecruiter: skipped entirely per task instructions (Indeed covered by another agent via connector; others out of scope for scraping).

- Not attempted this run (time/tool-budget, not a technical failure): relocate.me, findajob.dwp.gov.uk, hiring.cafe, studentcircus.com, totaljobs.com, cwjobs.co.uk, welcometothejungle.com, applied.com, Google Jobs via firecrawl_search (blocked - see Firecrawl entry above), workatastartup.com, joblift, myvisajobs.com, weworkremotely.com, remoteleaf. A follow-up pass should hit these, ideally once Firecrawl credits reset.

