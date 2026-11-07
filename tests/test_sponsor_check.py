import csv
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

import sponsor_check as sc

FIXTURE = os.path.join(os.path.dirname(__file__), "fixtures", "register_sample.csv")


class NormaliseNameTests(unittest.TestCase):
    def test_lowercases_and_drops_legal_suffix(self):
        self.assertEqual(sc.normalise_name("Northwind Analytics Ltd"), "northwind analytics")

    def test_drops_multi_word_suffix(self):
        self.assertEqual(
            sc.normalise_name("British Telecommunications Public Limited Company"),
            "british telecommunications",
        )

    def test_drops_bracketed_trailing_uk(self):
        self.assertEqual(sc.normalise_name("Acme (UK) Limited"), "acme")

    def test_ampersand_becomes_and_and_leading_the_goes(self):
        self.assertEqual(
            sc.normalise_name("The Marks & Spencer Group plc"), "marks and spencer group"
        )

    def test_folds_accents(self):
        self.assertEqual(sc.normalise_name("Société Lumière"), "societe lumiere")

    def test_dots_and_apostrophes_join_letters(self):
        self.assertEqual(sc.normalise_name("J.P. Morgan's"), "jp morgans")

    def test_hyphens_become_spaces(self):
        self.assertEqual(sc.normalise_name("Rolls-Royce plc"), "rolls royce")

    def test_drops_trailing_and_co(self):
        self.assertEqual(sc.normalise_name("Smith & Co."), "smith")

    def test_keeps_a_name_made_only_of_suffix_words(self):
        self.assertEqual(sc.normalise_name("UK Ltd"), "uk")


class ParseRatingTests(unittest.TestCase):
    def test_reads_letter_ratings_from_register_values(self):
        cases = {
            "Worker (A rating)": "A",
            "Temporary Worker (A rating)": "A",
            "Worker (A (Premium))": "A",
            "Worker (B rating)": "B",
        }
        for raw, want in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(sc.parse_rating(raw), want)

    def test_provisional_licence_has_no_letter_rating(self):
        self.assertIsNone(sc.parse_rating("Worker (UK Expansion Worker: Provisional )"))


class RouteTests(unittest.TestCase):
    def test_only_the_skilled_worker_route_counts(self):
        cases = {
            "Skilled Worker": True,
            " skilled worker ": True,
            "Creative Worker": False,
            "Global Business Mobility: Senior or Specialist Worker": False,
            "Scale-up": False,
        }
        for route, want in cases.items():
            with self.subTest(route=route):
                self.assertIs(sc.is_skilled_worker_route(route), want)


class SplitTradingNamesTests(unittest.TestCase):
    def test_splits_t_a_names(self):
        self.assertEqual(
            sc.split_trading_names("Oakridge Holdings Limited t/a Oakridge Coffee"),
            ["Oakridge Holdings Limited", "Oakridge Coffee"],
        )

    def test_splits_bracketed_trading_as(self):
        self.assertEqual(
            sc.split_trading_names("Alpha Ltd (trading as Beta)"), ["Alpha Ltd", "Beta"]
        )

    def test_leaves_plain_names_alone(self):
        self.assertEqual(sc.split_trading_names("Plain Name Ltd"), ["Plain Name Ltd"])


def write_file(folder, name, text, encoding="utf-8"):
    path = os.path.join(folder, name)
    with open(path, "w", encoding=encoding, newline="") as handle:
        handle.write(text)
    return path


class RegisterLoadingTests(unittest.TestCase):
    def test_groups_rows_by_organisation(self):
        register = sc.Register.from_csv(FIXTURE)
        self.assertEqual(register.row_count, 14)
        self.assertEqual(len(register.organisations), 13)

    def test_accepts_byte_order_mark_and_untidy_headers(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(
                tmp,
                "register.csv",
                " organisation name ,Town/City,County, Type & Rating ,ROUTE\n"
                "Pinecone Labs Ltd,York,,Worker (A rating),Skilled Worker\n",
                encoding="utf-8-sig",
            )
            register = sc.Register.from_csv(path)
        self.assertEqual(register.lookup("Pinecone Labs").grade, "CLEARED")

    def test_missing_required_column_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(tmp, "register.csv", "Organisation Name,Town/City\nPinecone Labs Ltd,York\n")
            with self.assertRaises(ValueError):
                sc.Register.from_csv(path)


class LookupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.register = sc.Register.from_csv(FIXTURE)

    def check(self, employer, **options):
        return self.register.lookup(employer, **options)

    def test_a_rated_skilled_worker_sponsor_is_cleared(self):
        result = self.check("northwind ANALYTICS limited")
        self.assertEqual(result.grade, "CLEARED")
        self.assertEqual(result.method, "exact")
        self.assertEqual(result.organisation.name, "Northwind Analytics Ltd")

    def test_every_route_for_an_organisation_is_reported(self):
        result = self.check("Northwind Analytics")
        self.assertEqual(result.organisation.routes, ["Creative Worker", "Skilled Worker"])

    def test_b_rated_skilled_worker_sponsor(self):
        self.assertEqual(self.check("Bluebell Care Homes").grade, "B_RATED")

    def test_sponsor_without_skilled_worker_route(self):
        self.assertEqual(self.check("Harbour Lights Theatre Company").grade, "OTHER_ROUTE")

    def test_provisional_expansion_worker_licence_is_not_skilled_worker(self):
        self.assertEqual(self.check("Ventral Systems").grade, "OTHER_ROUTE")

    def test_trading_name_in_register_matches_exactly(self):
        result = self.check("Oakridge Coffee")
        self.assertEqual(result.grade, "CLEARED")
        self.assertEqual(result.organisation.name, "Oakridge Holdings Limited t/a Oakridge Coffee")

    def test_spacing_differences_still_match_exactly(self):
        self.assertEqual(self.check("Hyperexponential").grade, "CLEARED")

    def test_accents_and_trailing_uk_still_match_exactly(self):
        self.assertEqual(self.check("Societe Lumiere").grade, "CLEARED")

    def test_brand_name_prefix_is_flagged_for_checking(self):
        result = self.check("Quillfeather")
        self.assertEqual(result.grade, "CHECK")
        self.assertEqual(result.method, "partial")
        self.assertEqual(result.organisation.name, "Quillfeather Bank Limited")

    def test_misspelt_name_is_flagged_not_cleared(self):
        result = self.check("Brightwatter Recruitment")
        self.assertEqual(result.grade, "CHECK")
        self.assertEqual(result.method, "fuzzy")
        self.assertEqual(result.organisation.name, "Brightwater Recruitment Ltd")

    def test_stricter_threshold_rejects_the_misspelling(self):
        self.assertEqual(self.check("Brightwatter Recruitment", threshold=0.99).grade, "NOT_FOUND")

    def test_two_entities_sharing_a_name_are_flagged(self):
        result = self.check("Kestrel Digital")
        self.assertEqual(result.grade, "CHECK")
        self.assertEqual(result.method, "ambiguous")
        self.assertEqual(
            sorted(org.name for org in result.candidates),
            ["Kestrel Digital Limited", "Kestrel Digital UK Ltd"],
        )

    def test_short_names_match_exactly_but_never_partially(self):
        self.assertEqual(self.check("Zeta").grade, "CLEARED")
        self.assertEqual(self.check("Arc").grade, "NOT_FOUND")

    def test_unknown_employer_is_not_found(self):
        result = self.check("Imaginary Widgets")
        self.assertEqual(result.grade, "NOT_FOUND")
        self.assertIsNone(result.organisation)


class ReadEmployersTests(unittest.TestCase):
    def test_text_file_skips_blank_lines_and_comments(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(tmp, "employers.txt", "Northwind Analytics\n\n# shortlist\n  Zeta  \n")
            records = sc.read_employers(path)
        self.assertEqual([r["employer"] for r in records], ["Northwind Analytics", "Zeta"])

    def test_csv_uses_company_column_and_keeps_title_and_url(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(
                tmp, "jobs.csv", "Job Title,Company,URL\nData Analyst,Zeta Ltd,https://example.com/1\n"
            )
            records = sc.read_employers(path)
        self.assertEqual(
            records,
            [{"employer": "Zeta Ltd", "title": "Data Analyst", "url": "https://example.com/1"}],
        )

    def test_csv_without_an_employer_column_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_file(tmp, "jobs.csv", "Title,Salary\nAnalyst,40000\n")
            with self.assertRaises(ValueError):
                sc.read_employers(path)

    def test_json_jobs_object(self):
        with tempfile.TemporaryDirectory() as tmp:
            text = json.dumps({"jobs": [{"company": "Zeta", "title": "Analyst", "url": "u"}]})
            records = sc.read_employers(write_file(tmp, "jobs.json", text))
        self.assertEqual(records, [{"employer": "Zeta", "title": "Analyst", "url": "u"}])

    def test_json_list_of_names(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = sc.read_employers(write_file(tmp, "jobs.json", json.dumps(["Zeta", "Arc Studios"])))
        self.assertEqual(
            records,
            [
                {"employer": "Zeta", "title": "", "url": ""},
                {"employer": "Arc Studios", "title": "", "url": ""},
            ],
        )


class CommandLineTests(unittest.TestCase):
    def test_writes_results_with_best_grades_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            employers = write_file(
                tmp,
                "employers.txt",
                "Imaginary Widgets\nQuillfeather\nNorthwind Analytics\nBluebell Care Homes\n",
            )
            out = os.path.join(tmp, "results.csv")
            with redirect_stdout(io.StringIO()):
                code = sc.main(["--register", FIXTURE, employers, "--out", out])
            with open(out, encoding="utf-8-sig", newline="") as handle:
                rows = list(csv.DictReader(handle))
        self.assertEqual(code, 0)
        self.assertEqual(
            [(row["employer"], row["grade"]) for row in rows],
            [
                ("Northwind Analytics", "CLEARED"),
                ("Quillfeather", "CHECK"),
                ("Bluebell Care Homes", "B_RATED"),
                ("Imaginary Widgets", "NOT_FOUND"),
            ],
        )
        self.assertEqual(rows[0]["register_name"], "Northwind Analytics Ltd")

    def test_employer_flag_prints_results_without_a_file(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = sc.main(["--register", FIXTURE, "--employer", "Zeta", "--employer", "Ventral Systems"])
        self.assertEqual(code, 0)
        self.assertIn("CLEARED", buffer.getvalue())
        self.assertIn("OTHER_ROUTE", buffer.getvalue())

    def test_no_employers_is_a_usage_error(self):
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit) as raised:
                sc.main(["--register", FIXTURE])
        self.assertEqual(raised.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
