"""Regression tests for command-line success and error paths."""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import unittest

from addon_doctor.cli import main


class CliTests(unittest.TestCase):
    def run_cli(self, argv: list[str]) -> tuple[int, str, str]:
        stdout = StringIO()
        stderr = StringIO()

        with redirect_stdout(stdout), redirect_stderr(stderr):
            result = main(argv)

        return result, stdout.getvalue(), stderr.getvalue()

    def test_auto_detection_failure_returns_usage_error(self) -> None:
        with patch("addon_doctor.cli.detect_addons_directory", return_value=None):
            result, stdout, stderr = self.run_cli([])

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("was not found automatically", stderr)

    def test_nonexistent_path_returns_scan_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / "missing"
            result, stdout, stderr = self.run_cli([str(missing)])

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("Scan failed:", stderr)

    def test_file_path_returns_scan_error(self) -> None:
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "not-a-directory.txt"
            file_path.write_text("not an AddOns directory", encoding="utf-8")
            result, stdout, stderr = self.run_cli([str(file_path)])

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("Scan failed:", stderr)

    def test_empty_directory_produces_an_empty_report(self) -> None:
        with TemporaryDirectory() as temp_dir:
            result, stdout, stderr = self.run_cli([temp_dir])

        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Unique add-on/library IDs: 0", stdout)
        self.assertIn("Manifest candidates: 0", stdout)

    def test_directory_without_manifests_produces_an_empty_report(self) -> None:
        with TemporaryDirectory() as temp_dir:
            addon = Path(temp_dir) / "Example"
            addon.mkdir()
            (addon / "README.txt").write_text("not a manifest", encoding="utf-8")
            result, stdout, stderr = self.run_cli([temp_dir])

        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Manifest candidates: 0", stdout)

    def test_invalid_utf8_is_replaced_without_crashing(self) -> None:
        with TemporaryDirectory() as temp_dir:
            addon = Path(temp_dir) / "Example"
            addon.mkdir()
            (addon / "Example.txt").write_bytes(
                b"## Title: Invalid \xff Title\n## APIVersion: 101050\n"
            )
            result, stdout, stderr = self.run_cli([temp_dir])

        self.assertEqual(result, 0)
        self.assertEqual(stderr, "")
        self.assertIn("Unique add-on/library IDs: 1", stdout)

    def test_permission_error_returns_scan_error(self) -> None:
        with patch(
            "addon_doctor.cli.build_text_report",
            side_effect=PermissionError("access denied"),
        ):
            result, stdout, stderr = self.run_cli(["C:\\ESO\\AddOns"])

        self.assertEqual(result, 2)
        self.assertEqual(stdout, "")
        self.assertIn("Scan failed: access denied", stderr)


if __name__ == "__main__":
    unittest.main()
