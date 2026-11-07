# visa-job-hunt

Check whether UK employers can sponsor a Skilled Worker visa, using the Home Office register of licensed sponsors.

Job adverts use trading names, but the register lists legal entity names, so a quick search often misses the employer or finds the wrong one. `sponsor_check.py` cleans up both sets of names, matches them, and gives each employer a grade. It only marks an employer as cleared on an exact match. Anything less certain is flagged for you to check.

Python 3.9 or later, with no other dependencies.

## Quick start

1. Download the latest register CSV ("Worker and Temporary Worker") from
   [GOV.UK](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers).
   It changes often, so get a fresh copy before each search.
2. Check a list of employers and save the results:

   ```bash
   python sponsor_check.py --register register.csv employers.txt --out results.csv
   ```

3. Or check one or two names straight from the command line:

   ```bash
   python sponsor_check.py --register register.csv --employer "Employer Name Ltd"
   ```

To see what it does before downloading anything, run it on the small fictional register used by the tests:

```bash
python sponsor_check.py --register tests/fixtures/register_sample.csv \
  --employer "Northwind Analytics" --employer "Quillfeather" \
  --employer "Bluebell Care Homes" --employer "Harbour Lights Theatre Company" \
  --employer "Imaginary Widgets"
```

```
CLEARED      Northwind Analytics -> Northwind Analytics Ltd
CHECK        Quillfeather -> Quillfeather Bank Limited
B_RATED      Bluebell Care Homes -> Bluebell Care Homes Limited
OTHER_ROUTE  Harbour Lights Theatre Company -> Harbour Lights Theatre Company Ltd
NOT_FOUND    Imaginary Widgets
```

## Input files

| File | Format |
|------|--------|
| `.txt` | One employer per line. Blank lines and lines starting with `#` are skipped. |
| `.csv` | A column called `company`, `employer` or `organisation`. Any `title` and `url` columns are copied into the results. |
| `.json` | A list of names, or `{"jobs": [{"company": "...", "title": "...", "url": "..."}]}`. |

## Grades

| Grade | Meaning |
|-------|---------|
| `CLEARED` | Exact name match, A-rated, and licensed for the Skilled Worker route. |
| `CHECK` | A possible match: a partial or fuzzy name match, or several register entries with the same name. Confirm the legal entity before relying on it. |
| `B_RATED` | Licensed for Skilled Worker but B-rated, so it can't assign new certificates of sponsorship until it's back to an A rating. |
| `OTHER_ROUTE` | On the register, but not for the Skilled Worker route. |
| `NOT_FOUND` | No match. If the company trades under another name, look up its legal name on Companies House and try that. |

The results CSV has one row per employer, best grades first. Each row has the matched register entry, its routes and ratings, how it matched, a similarity score and a short note.

## How matching works

- Names are lowercased, accents are removed, `&` becomes "and", and a leading "The" and trailing legal words (Ltd, Limited, PLC, LLP, Inc, UK and similar) are dropped. "The Marks & Spencer Group plc" becomes `marks and spencer group`.
- Register entries written as "X Ltd t/a Y" or "X Ltd (trading as Y)" can be found under either name.
- An exact match is the only kind that can be `CLEARED`. Exact matching ignores spacing, so "Hyperexponential" finds "Hyper Exponential Ltd".
- Otherwise the tool looks for register names that start with yours ("Quillfeather" finds "Quillfeather Bank Limited") and for close spellings, with a similarity of 0.88 or more by default (change it with `--threshold`). These are always `CHECK`.
- Names shorter than 5 letters are only matched exactly, because short names produce too many false matches.

## Limits

- Being on the register means an employer can sponsor, not that it will sponsor you. The job also has to meet the Skilled Worker salary and occupation rules.
- The tool can't link a brand to a legal name that looks nothing like it. Companies House is the place to look those up.
- This isn't legal or immigration advice.

## Tests

```bash
python -m unittest
```

## Licence

MIT. See [LICENSE](LICENSE).
