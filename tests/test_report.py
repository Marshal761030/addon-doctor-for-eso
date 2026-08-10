from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from addon_doctor.report import build_text_report


class ReportTests(unittest.TestCase):
    def test_report_contains_dependency_findings_and_duplicates(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            owner = root / "Owner"
            owner.mkdir()
            (owner / "Owner.txt").write_text(
                "## Title: Owner\n"
                "## DependsOn: LibA>=20 MissingLib\n"
                "## OptionalDependsOn: OptionalLib\n",
                encoding="utf-8",
            )

            lib = root / "LibA"
            lib.mkdir()
            for suffix in (".txt", ".addon"):
                (lib / f"LibA{suffix}").write_text(
                    "## Title: LibA\n## AddOnVersion: 10\n## IsLibrary: true\n",
                    encoding="utf-8",
                )

            report = build_text_report(root)

        self.assertIn("VERSION_TOO_OLD", report)
        self.assertIn("MISSING", report)
        self.assertIn("OPTIONAL_MISSING", report)
        self.assertIn("LibA:", report)
        self.assertIn("does not upload", report)


if __name__ == "__main__":
    unittest.main()
