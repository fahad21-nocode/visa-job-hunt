# Failures / blocked sources log (discovery run 2)

## firecrawl.dev (mcp__Firecrawl__firecrawl_search / firecrawl_scrape / firecrawl_map) — session-wide outage
All 7 Firecrawl calls attempted at the start of this run (firecrawl_search against ukvisajobs.com, huntukvisasponsors.com, relocate.me, findajob.dwp.gov.uk and hiring.cafe) failed immediately with "Insufficient credits for this connected-app request" — the account's daily MCP credit allowance was exhausted before this session started, and another agent running in parallel confirmed the same outage independently. Per the coordinator's instruction, stopped retrying Firecrawl entirely for the rest of the run and switched to `mcp__string__web_access_search` / `mcp__string__web_access_fetch` (a Google-backed search+fetch tool) and `mcp__foundrole__jobs_search` instead. Firecrawl was not retried again after the first failure.

## ukvisajobs.com
Direct fetch of `/jobs?q=data+analyst` returned a 404 (site's own "page not found" SPA shell, `jobs_count: 18332` visible in the embedded JSON so the site itself is live) — the query-string search pattern tried does not match the site's real search route, which appears to require client-side JS routing not reachable via a plain fetch. No usable listing retrieved from this domain this run.

## boards.greenhouse.io / jobs.lever.co
No direct ATS-API calls made. Google-indexed search for `site:boards.greenhouse.io` and `site:jobs.lever.co` against the target role families returned zero results, and none of the UK SaaS employers already found in this run (Workiva, HubSpot, Sinch, Pure Storage, Claroty, IP Fabric) were confirmed to run their EMEA/UK career pages on Greenhouse or Lever rather than Workday/SuccessFactors/custom ATS, so no board slugs were guessed. Logged as not attempted rather than a false negative — a future run with more time could check each employer's own careers page footer for the real ATS before trying the JSON endpoint.

## findajob.dwp.gov.uk, hiring.cafe, relocate.me
All three returned zero or near-zero usable UK postings for the target role families via Google-indexed search (relocate.me surfaced only its own generic country/company index pages, not individual UK job ads). Not retried with a plain-HTTP fetch of the sites' own search pages due to time; flagged for a future run.

## studentcircus.com, totaljobs.com, cwjobs.co.uk, welcometothejungle.com, applied.com, workatastartup.com, myvisajobs.com, weworkremotely.com, remoteleaf, joblift
Not reached this run — time was spent on the sources that did yield results (huntukvisasponsors.com, FoundRole). None of these returned any hits in the generic Google-search sweep either (results were almost entirely Indeed/LinkedIn/Glassdoor SERP noise, which is explicitly out of scope per instructions). Flagged for a retry pass in a future session.
