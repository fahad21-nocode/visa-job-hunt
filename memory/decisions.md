# Decisions log

Dated, append-only. Record anything that changes how the agent behaves,
not routine run output.

## 2026-11-12 — `/strategy-reset` applied

Workspace built green-field (no prior career-ops files existed in this
repository). Established: auto-apply/auto-send off, weekly cap of 10,
tooling freeze until 17 Feb 2027, priority consultancy/outsourcer channel
swept first, TSL-window tagging and 3.5/5 interim apply gate for RQF 3–5
roles until 31 Dec 2026, sponsorship-first-contact question, warm-intro
check before apply, R3/R4 as parallel tracks. See
`memory/runs/strategy-reset-20261112-1216.md` for the full run report.

## 2026-11-12 — Scrapling unavailable in this sandbox, substituted Firecrawl

`career-ops-rules.md` §2 specifies the Scrapling skill for visa-sponsorship
searches. Scrapling itself installed cleanly via the documented npx
command, but this cloud session's network proxy only allows a pre-approved
host allowlist, so direct HTTP requests to company domains (e.g.
www.infosys.com) are refused by the proxy before reaching the site at all
— a sandbox network constraint, not a robots.txt or anti-bot block, and
not something to try to route around. Substituted Firecrawl's MCP tools
(`firecrawl_search`/`firecrawl_scrape`), which proxy through their own
infrastructure, for this run's portal sweep. Flagging per the rule that a
substitution away from Scrapling must be stated, not silent. A future
session running outside this sandbox's proxy restrictions, or with the
allowlist widened, should retry Scrapling directly.

## Scheduled — 2027-01-01 (not yet executed)

Revert the RQF 3–5 apply gate from 3.5/5 to 4.0/5 (`career-ops-rules.md`
§4, `opencode.json agent.apply_gate.rqf_3_5`). The agent does this on its
own on or after that date and logs the actual reversion here with the
date it ran.
