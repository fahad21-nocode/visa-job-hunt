#!/usr/bin/env python3
"""Check UK employers against the Home Office register of licensed sponsors.

Job adverts use trading names; the register lists legal entity names. This
tool normalises both, matches them, and grades each employer on whether it
can sponsor a Skilled Worker visa. It never marks a guess as cleared.

    python sponsor_check.py --register register.csv employers.txt --out results.csv
    python sponsor_check.py --register register.csv --employer "Monzo Bank"
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict
from dataclasses import dataclass, field
from difflib import SequenceMatcher
from typing import Dict, List, Optional, Sequence, Set, Tuple

CLEARED = "CLEARED"
CHECK = "CHECK"
B_RATED = "B_RATED"
OTHER_ROUTE = "OTHER_ROUTE"
NOT_FOUND = "NOT_FOUND"
GRADE_ORDER = (CLEARED, CHECK, B_RATED, OTHER_ROUTE, NOT_FOUND)

DEFAULT_THRESHOLD = 0.88
MIN_FUZZY_LENGTH = 5
MAX_CANDIDATES = 3

# Trailing words that describe a company's legal form rather than its name.
# Longer phrases come first so "Public Limited Company" goes in one step.
_LEGAL_SUFFIXES = [
    ("public", "limited", "company"),
    ("limited", "liability", "partnership"),
    ("community", "interest", "company"),
    ("limited", "company"),
    ("limited",),
    ("ltd",),
    ("plc",),
    ("llp",),
    ("lp",),
    ("llc",),
    ("inc",),
    ("incorporated",),
    ("corporation",),
    ("corp",),
    ("company",),
    ("co",),
    ("cic",),
    ("uk",),
    ("gb",),
    ("and",),
]

_JOINING_PUNCTUATION = re.compile(r"[.'’`]")
_OTHER_PUNCTUATION = re.compile(r"[^a-z0-9]+")
_RATING = re.compile(r"\(\s*([AB])\b")
_TRADING_AS = re.compile(r"\s*\(?\s*\b(?:t\s*/\s*a|trading\s+as)\b\s*", re.IGNORECASE)
_STOPWORDS = {"a", "and", "at", "for", "in", "of", "on", "the", "to"}

_REGISTER_COLUMNS = {
    "name": ("organisation name", "organization name", "name"),
    "town": ("town/city", "town", "city"),
    "county": ("county",),
    "type_rating": ("type & rating", "type and rating", "rating"),
    "route": ("route",),
}
_REQUIRED_REGISTER_COLUMNS = {
    "name": "Organisation Name",
    "type_rating": "Type & Rating",
    "route": "Route",
}
_EMPLOYER_COLUMNS = {
    "employer": (
        "company",
        "employer",
        "organisation",
        "organization",
        "company name",
        "employer name",
        "organisation name",
        "organization name",
    ),
    "title": ("title", "job title", "role", "position"),
    "url": ("url", "link", "job url", "job link"),
}
_JSON_EMPLOYER_KEYS = ("company", "employer", "organisation", "organization")

RESULT_COLUMNS = [
    "employer",
    "title",
    "url",
    "grade",
    "register_name",
    "town",
    "county",
    "routes",
    "ratings",
    "match",
    "score",
    "note",
]

_NOT_FOUND_NOTE = (
    "No matching employer on the register. If the company trades under another "
    "name, look up its legal name on Companies House and check that."
)
_SHORT_NAME_NOTE = (
    "No exact match. Names under 5 letters are only matched exactly, so try the "
    "employer's full legal name."
)
_STATUS_TEXT = {
    "A": "A-rated for Skilled Worker",
    "B": "B-rated for Skilled Worker",
    "unknown": "Skilled Worker licence, rating unclear",
    "none": "not licensed for Skilled Worker",
}
_STATUS_RANK = {"A": 0, "unknown": 1, "B": 2, "none": 3}


def normalise_name(name: str) -> str:
    """Reduce an organisation name to a comparable key.

    Lowercases, folds accents, turns "&" into "and", drops a leading "the"
    and trailing legal-form words (Ltd, PLC, LLP, UK ...). A name made only
    of such words keeps its last word rather than vanishing.
    """
    text = unicodedata.normalize("NFKD", name or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch)).lower()
    text = text.replace("&", " and ").replace("+", " and ")
    text = _JOINING_PUNCTUATION.sub("", text)
    tokens = _OTHER_PUNCTUATION.sub(" ", text).split()

    if len(tokens) > 1 and tokens[0] == "the":
        tokens = tokens[1:]

    stripped = True
    while stripped:
        stripped = False
        for suffix in _LEGAL_SUFFIXES:
            size = len(suffix)
            if len(tokens) > size and tuple(tokens[-size:]) == suffix:
                tokens = tokens[:-size]
                stripped = True
                break
    return " ".join(tokens)


def parse_rating(type_and_rating: str) -> Optional[str]:
    """Return "A" or "B" from a register "Type & Rating" value, else None."""
    match = _RATING.search(type_and_rating or "")
    return match.group(1) if match else None


def is_skilled_worker_route(route: str) -> bool:
    """True when a register "Route" value is the Skilled Worker route."""
    return "skilled worker" in " ".join((route or "").lower().split())


def split_trading_names(name: str) -> List[str]:
    """Split "X Ltd t/a Y" or "X Ltd (trading as Y)" into ["X Ltd", "Y"]."""
    parts = (part.strip(" ()") for part in _TRADING_AS.split(name or ""))
    return [part for part in parts if part]


@dataclass
class Organisation:
    """One organisation on the register, with every licence row it holds."""

    name: str
    town: str = ""
    county: str = ""
    licences: List[Tuple[str, str]] = field(default_factory=list)

    @property
    def routes(self) -> List[str]:
        return sorted({route for _, route in self.licences if route})

    @property
    def ratings(self) -> List[str]:
        return sorted({rating for rating, _ in self.licences if rating})

    @property
    def skilled_worker_status(self) -> str:
        """"A", "B", "unknown" (licensed, no letter rating) or "none"."""
        ratings = {
            parse_rating(rating)
            for rating, route in self.licences
            if is_skilled_worker_route(route)
        }
        if not ratings:
            return "none"
        if "A" in ratings:
            return "A"
        if "B" in ratings:
            return "B"
        return "unknown"

    def describe(self) -> str:
        place = self.town or "town not listed"
        return f"{self.name} ({place}, {_STATUS_TEXT[self.skilled_worker_status]})"


@dataclass
class Result:
    """The outcome of checking one employer name."""

    employer: str
    grade: str
    method: str  # exact, ambiguous, partial, fuzzy or none
    score: float
    candidates: List[Organisation] = field(default_factory=list)
    note: str = ""

    @property
    def organisation(self) -> Optional[Organisation]:
        return self.candidates[0] if self.candidates else None


class Register:
    """The sponsor register, indexed for name lookups."""

    def __init__(self, organisations: Sequence[Organisation], row_count: Optional[int] = None):
        self.organisations = list(organisations)
        if row_count is None:
            row_count = sum(len(org.licences) for org in self.organisations)
        self.row_count = row_count
        self._keys: List[List[str]] = []
        self._exact: Dict[str, Set[int]] = defaultdict(set)
        self._tokens: Dict[str, Set[int]] = defaultdict(set)
        self._prefixes: Dict[str, Set[int]] = defaultdict(set)
        for index, organisation in enumerate(self.organisations):
            keys: List[str] = []
            for part in split_trading_names(organisation.name):
                key = normalise_name(part)
                if key and key not in keys:
                    keys.append(key)
            self._keys.append(keys)
            for key in keys:
                compact = key.replace(" ", "")
                self._exact[key].add(index)
                self._exact[compact].add(index)
                self._prefixes[compact[:4]].add(index)
                for token in _index_tokens(key):
                    self._tokens[token].add(index)

    @classmethod
    def from_csv(cls, path: str) -> "Register":
        """Load the Home Office "Worker and Temporary Worker" register CSV."""
        rows = csv.reader(io.StringIO(_read_text(path)))
        header = next(rows, None)
        if not header:
            raise ValueError(f"{path} is empty.")
        columns = _find_columns(header, _REGISTER_COLUMNS)
        missing = [label for key, label in _REQUIRED_REGISTER_COLUMNS.items() if key not in columns]
        if missing:
            raise ValueError(
                f"{path} is missing the column(s) {', '.join(missing)}. "
                "Use the Home Office 'Worker and Temporary Worker' register CSV."
            )
        organisations: Dict[Tuple[str, str], Organisation] = {}
        row_count = 0
        for row in rows:
            name = _cell(row, columns["name"])
            if not name:
                continue
            row_count += 1
            town = _cell(row, columns.get("town"))
            organisation = organisations.get((name, town.lower()))
            if organisation is None:
                organisation = Organisation(name, town, _cell(row, columns.get("county")))
                organisations[(name, town.lower())] = organisation
            organisation.licences.append(
                (_cell(row, columns["type_rating"]), _cell(row, columns["route"]))
            )
        return cls(list(organisations.values()), row_count)

    def lookup(self, employer: str, threshold: float = DEFAULT_THRESHOLD) -> Result:
        """Match one employer name against the register and grade it."""
        key = normalise_name(employer)
        if not key:
            return Result(employer, NOT_FOUND, "none", 0.0, note="No employer name given.")
        compact = key.replace(" ", "")
        hits = self._exact.get(key, set()) | self._exact.get(compact, set())
        if hits:
            return _grade_exact(employer, [self.organisations[i] for i in sorted(hits)])
        if len(compact) < MIN_FUZZY_LENGTH:
            return Result(employer, NOT_FOUND, "none", 0.0, note=_SHORT_NAME_NOTE)

        matches = self._near_matches(key, compact, threshold)
        if not matches:
            return Result(employer, NOT_FOUND, "none", 0.0, note=_NOT_FOUND_NOTE)
        _, method, score = matches[0]
        candidates = [organisation for organisation, _, _ in matches[:MAX_CANDIDATES]]
        if len(matches) == 1:
            note = (
                f"Possible match: {candidates[0].describe()}. "
                "Confirm it's the same legal entity before relying on it."
            )
        else:
            listed = "; ".join(org.describe() for org in candidates)
            note = (
                f"{len(matches)} possible matches, closest first: {listed}. "
                "Confirm which legal entity is hiring."
            )
        return Result(employer, CHECK, method, round(score, 2), candidates, note)

    def _near_matches(
        self, key: str, compact: str, threshold: float
    ) -> List[Tuple[Organisation, str, float]]:
        candidates = set(self._prefixes.get(compact[:4], ()))
        for token in _index_tokens(key):
            candidates |= self._tokens.get(token, set())

        best: Dict[int, Tuple[str, float]] = {}
        for index in candidates:
            for register_key in self._keys[index]:
                if register_key.startswith(key + " "):
                    found = ("partial", _ratio(key, register_key))
                else:
                    score = _similarity(key, register_key, threshold)
                    if score < threshold:
                        continue
                    found = ("fuzzy", score)
                if index not in best or found[1] > best[index][1]:
                    best[index] = found

        ranked = sorted(
            best.items(), key=lambda item: (-item[1][1], self.organisations[item[0]].name)
        )
        return [(self.organisations[index], method, score) for index, (method, score) in ranked]


def _grade_exact(employer: str, organisations: List[Organisation]) -> Result:
    if len(organisations) == 1:
        organisation = organisations[0]
        status = organisation.skilled_worker_status
        if status == "A":
            grade = CLEARED
            note = (
                "A-rated for the Skilled Worker route. The job itself still has to "
                "meet the Skilled Worker salary and occupation rules."
            )
        elif status == "B":
            grade = B_RATED
            note = (
                "Licensed for Skilled Worker but B-rated, so it can't assign new "
                "certificates of sponsorship until it's back to an A rating."
            )
        elif status == "unknown":
            grade = CHECK
            note = "Licensed for Skilled Worker, but the register shows no A or B rating."
        else:
            grade = OTHER_ROUTE
            routes = ", ".join(organisation.routes) or "no route listed"
            note = f"On the register, but not for the Skilled Worker route (licensed for: {routes})."
        return Result(employer, grade, "exact", 1.0, [organisation], note)

    ordered = sorted(
        organisations, key=lambda org: (_STATUS_RANK[org.skilled_worker_status], org.name)
    )
    statuses = {org.skilled_worker_status for org in ordered}
    if statuses == {"none"}:
        grade = OTHER_ROUTE
    elif statuses <= {"B", "none"}:
        grade = B_RATED
    else:
        grade = CHECK
    listed = "; ".join(org.describe() for org in ordered[:MAX_CANDIDATES])
    note = (
        f"{len(ordered)} register entries match this name: {listed}. "
        "Confirm which legal entity is hiring."
    )
    return Result(employer, grade, "ambiguous", 1.0, ordered[:MAX_CANDIDATES], note)


def _index_tokens(key: str) -> List[str]:
    return [token for token in key.split() if len(token) > 1 and token not in _STOPWORDS]


def _ratio(left: str, right: str) -> float:
    return SequenceMatcher(None, left, right, autojunk=False).ratio()


def _similarity(left: str, right: str, threshold: float) -> float:
    """Best of a plain, a space-free and a word-order-free comparison."""
    pairs = (
        (left, right),
        (left.replace(" ", ""), right.replace(" ", "")),
        (" ".join(sorted(left.split())), " ".join(sorted(right.split()))),
    )
    best = 0.0
    for a, b in pairs:
        matcher = SequenceMatcher(None, a, b, autojunk=False)
        if matcher.real_quick_ratio() < threshold or matcher.quick_ratio() < threshold:
            continue
        best = max(best, matcher.ratio())
    return best


def _read_text(path: str) -> str:
    with open(path, "rb") as handle:
        raw = handle.read()
    try:
        return raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        return raw.decode("cp1252", errors="replace")


def _header_key(text: str) -> str:
    return " ".join((text or "").replace("﻿", "").strip().lower().split())


def _find_columns(header: Sequence[str], wanted: Dict[str, Tuple[str, ...]]) -> Dict[str, int]:
    positions = {_header_key(name): index for index, name in enumerate(header)}
    found: Dict[str, int] = {}
    for field_name, aliases in wanted.items():
        for alias in aliases:
            if alias in positions:
                found[field_name] = positions[alias]
                break
    return found


def _cell(row: Sequence[str], index: Optional[int]) -> str:
    if index is None or index >= len(row):
        return ""
    return row[index].strip()


def read_employers(path: str) -> List[Dict[str, str]]:
    """Read employers from a .txt (one per line), .csv or .json file."""
    text = _read_text(path)
    extension = os.path.splitext(path)[1].lower()

    if extension == ".csv":
        rows = csv.reader(io.StringIO(text))
        columns = _find_columns(next(rows, None) or [], _EMPLOYER_COLUMNS)
        if "employer" not in columns:
            raise ValueError(f"{path} needs a column called company, employer or organisation.")
        records = []
        for row in rows:
            employer = _cell(row, columns["employer"])
            if employer:
                records.append(
                    {
                        "employer": employer,
                        "title": _cell(row, columns.get("title")),
                        "url": _cell(row, columns.get("url")),
                    }
                )
        return records

    if extension == ".json":
        data = json.loads(text)
        items = data.get("jobs", []) if isinstance(data, dict) else data
        if not isinstance(items, list):
            raise ValueError(f"{path} should hold a list, or an object with a \"jobs\" list.")
        records = []
        for item in items:
            if isinstance(item, str):
                record = {"employer": item.strip(), "title": "", "url": ""}
            elif isinstance(item, dict):
                fields = {str(k).lower(): v for k, v in item.items()}
                employer = next(
                    (str(fields[k]).strip() for k in _JSON_EMPLOYER_KEYS if fields.get(k)), ""
                )
                record = {
                    "employer": employer,
                    "title": str(fields.get("title") or "").strip(),
                    "url": str(fields.get("url") or "").strip(),
                }
            else:
                continue
            if record["employer"]:
                records.append(record)
        return records

    return [
        {"employer": line.strip(), "title": "", "url": ""}
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]


def write_results(path: str, results: List[Tuple[Dict[str, str], Result]]) -> None:
    """Write checked employers to a CSV that opens cleanly in Excel."""
    with open(path, "w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_COLUMNS)
        writer.writeheader()
        for record, result in results:
            organisation = result.organisation
            writer.writerow(
                {
                    "employer": record["employer"],
                    "title": record.get("title", ""),
                    "url": record.get("url", ""),
                    "grade": result.grade,
                    "register_name": organisation.name if organisation else "",
                    "town": organisation.town if organisation else "",
                    "county": organisation.county if organisation else "",
                    "routes": "; ".join(organisation.routes) if organisation else "",
                    "ratings": "; ".join(organisation.ratings) if organisation else "",
                    "match": result.method,
                    "score": f"{result.score:.2f}",
                    "note": result.note,
                }
            )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sponsor_check.py",
        description="Check UK employers against the Home Office register of licensed sponsors.",
    )
    parser.add_argument(
        "employers", nargs="?", help="a .txt, .csv or .json file of employers or job adverts"
    )
    parser.add_argument(
        "--register", required=True, help="the Home Office 'Worker and Temporary Worker' CSV"
    )
    parser.add_argument(
        "--employer",
        action="append",
        default=[],
        metavar="NAME",
        help="an employer to check; repeat for more",
    )
    parser.add_argument("--out", help="also write the results to this CSV file")
    parser.add_argument(
        "--threshold",
        type=float,
        default=DEFAULT_THRESHOLD,
        help="fuzzy-match cut-off between 0 and 1 (default %(default)s)",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.employers and not args.employer:
        parser.error("give a file of employers, or at least one --employer")
    if not 0 < args.threshold <= 1:
        parser.error("--threshold must be between 0 and 1")

    try:
        register = Register.from_csv(args.register)
        records = read_employers(args.employers) if args.employers else []
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    records += [{"employer": name, "title": "", "url": ""} for name in args.employer]

    results = [(record, register.lookup(record["employer"], args.threshold)) for record in records]
    results.sort(key=lambda pair: GRADE_ORDER.index(pair[1].grade))

    for record, result in results:
        target = f" -> {result.organisation.name}" if result.organisation else ""
        print(f"{result.grade:<12} {record['employer']}{target}")

    counts = {grade: 0 for grade in GRADE_ORDER}
    for _, result in results:
        counts[result.grade] += 1
    summary = ", ".join(f"{counts[grade]} {grade}" for grade in GRADE_ORDER if counts[grade])
    print(
        f"\nChecked {len(results)} employer(s) against "
        f"{len(register.organisations):,} organisations on the register: {summary}."
    )
    if args.out:
        write_results(args.out, results)
        print(f"Results written to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
