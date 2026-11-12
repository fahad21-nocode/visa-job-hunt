# Intel

Free-form market/employer intelligence notes. Append dated entries; don't
overwrite earlier ones. Verify any sponsor-licence, SOC-code or salary
fact here against the live tools before relying on it — this file is
notes, not a source of truth for Gates 1/2.

## 2026-11-12 — priority employer Gate 1 pass

Ran Gate 1 against all 15 seeded `priority_employers.csv` brands using
the live sponsor-register tools (not from memory). 14 of 15 confirmed
A-rated with the Skilled Worker route current today. One finding worth
flagging: **LTIMindtree UK Limited was removed from the register on
2026-09-01** — it was A-rated before removal but is not currently a
licensed sponsor. Don't pursue LTIMindtree on R1 until re-verified; it
may still be worth an R2/R3/R4 look, or a direct ask whether a different
LTIMindtree entity now sponsors.

Several brands have sister/related UK entities also on the register that
weren't individually verified this run (Infosys Fluido UK LTD, Infosys
Tech Solutions Ltd, Wipro Appirio UK Limited, Wipro Connected Services UK
Limited, Cognizant Business Logics Limited, NTT Data Business Solutions
Limited, NTT DATA Services UK Limited, KPMG IFRG Ltd, KPMG LLP (Local
Hires), KPMG US Tax Service (London) LLP, PricewaterhouseCoopers
(Northern Ireland) LLP). Worth checking individually if a role surfaces
under one of those names.

## 2026-11-12 — first live role search via FoundRole

Ran the priority-channel keywords (SuccessFactors support/AMS, HRIS
support, HR operations analyst, application support analyst) against the
14 cleared priority employers via FoundRole (`jobs_search`), per Fahad's
go-ahead to use available connectors since the Scrapling skill isn't
installed in this session. Four distinct queries surfaced 5 roles at 4
employers (NTT Global Data Centers Americas Inc, Accenture, Wipro,
HCLTech ×2) — all scored `don't-apply` or `need-info`: two are senior
Workday-configuration roles (a stated profile gap), two are HCLTech
postings whose actual duties (entry-level robotics teleoperation; senior
data architecture) don't match their listed titles at all, and one (Wipro
AV Support Engineer) is too thin a posting to score. None are genuine
SuccessFactors/HRIS-support/HR-ops-analyst-level matches.

Read on this: FoundRole's UK coverage for this specific niche (HR-tech
support/AMS roles at IT consultancies) looks thin so far, or the
keywords need adjusting. Worth trying Indeed directly for the same
keywords, and/or checking each employer's own careers site/ATS, before
concluding the channel itself is weak — one day of FoundRole results
isn't enough signal either way.
