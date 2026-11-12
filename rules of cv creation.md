# Rules of CV creation

Standalone process for CV, cover letter and application-answer work.
`career-ops-rules.md` wins on rules if the two ever conflict. `/sponsor-sweep`
never runs this process — it finds roles only.

## Inputs

Two inputs are required before any stage runs: the CV text and the target
job description. Without a JD there is nothing to diff against, so stages
2 and 4 are meaningless. Stop and ask rather than inventing a JD.

## Five stages (run in order)

1. **Diagnoser.** Scan as an ATS would. Flag formatting, layout and
   section-header parsing traps.
2. **Recruiter.** Build a table of required skills vs stated experience,
   each marked HAVE / PARTIAL / GAP. Quote the CV evidence for every HAVE.
   List the top 5 missing technical keywords and top 5 missing soft
   keywords. Name three professional gaps or red flags.
3. **Rewriter.** Put every bullet in STAR form (Situation, Task, Action,
   Result), compressed to one line and led by the Result. Quantify it and
   put JD keywords in the Action. XYZ phrasing ("Accomplished X, as
   measured by Y, by doing Z") is fine where it reads better, as long as
   the Result leads and all four STAR elements are recoverable.
4. **ATS Simulator — blocking gate.** Give a match score /100. Check
   keyword density for both under-use and stuffing. Simulate the
   field-by-field parse, check section recognition, and list remaining
   formatting risks. Verdict: PASS / FIX / DON'T-APPLY. On FIX, fix and
   re-run until it passes, then output clean optimised markdown. No human
   sees the CV before this passes.
5. **Hiring Manager.** Only after stage 4 passes. Ask the 5 hardest
   questions one at a time, score each answer /10, and probe the stage-2
   red flags directly.

## Content rules

- The CV reads as the target role, not the held title (coordinator →
  analyst reframe). Skills mirror the target role's language.
- Summary = years + specialty + one hard metric.
- Quantify every bullet in plain figures — never "c.", "circa", "around",
  "approx." or "~" in front of a number.
- Skills list mirrors exact JD terms. Coherent upward arc. Two pages is
  fine.
- Put technical skills (SQL, Python, Power BI, automation) alongside the
  HR domain toolkit where relevant.
- Certification line: "SAP SuccessFactors Employee Central Core
  (C_THR81) — scheduled [month] 2026". Never mark it held or passed until
  a credential ID and pass date are provided.
- No "Selected Builds" section and no named personal projects. PeopleStack
  appears only as a normal experience entry, described generically.
- Never invent metrics, dates or employers. If a bullet needs a number he
  hasn't given, ask for it or leave a clearly marked placeholder.

## Rendering

WeasyPrint HTML-to-PDF: single-column A4, navy #1F4E78 accents, Liberation
Sans, em-dash bullets. Contact details and LinkedIn go in the header
exactly as he supplies them.
