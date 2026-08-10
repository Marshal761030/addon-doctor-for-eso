from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from addon_doctor.inventory import build_inventory, find_manifest_paths


class InventoryTests(unittest.TestCase):
    def test_uses_nested_scan_window_and_matching_directory_names(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            first = root / "First"
            first.mkdir()
            (first / "First.txt").write_text(
                "## Title: First\n## APIVersion: 101050\n", encoding="utf-8"
            )
            (first / "ReadMe.txt").write_text(
                "## Title: Not A Manifest\n## APIVersion: 101050\n",
                encoding="utf-8",
            )

            second = root / "Container" / "Second"
            second.mkdir(parents=True)
            (second / "Second.addon").write_text(
                "## Title: Second\n## IsLibrary: true\n", encoding="utf-8"
            )

            third = root / "Container" / "Middle" / "Third"
            third.mkdir(parents=True)
            (third / "Third.txt").write_text(
                "## Title: Third\n## APIVersion: 101050\n", encoding="utf-8"
            )

            too_deep = root / "A" / "B" / "C" / "Fourth"
            too_deep.mkdir(parents=True)
            (too_deep / "Fourth.txt").write_text(
                "## Title: Fourth\n## APIVersion: 101050\n", encoding="utf-8"
            )

            paths = find_manifest_paths(root)
            inventory = build_inventory(root)

        self.assertEqual(len(paths), 3)
        self.assertIn("First", inventory)
        self.assertIn("Second", inventory)
        self.assertIn("Third", inventory)
        self.assertNotIn("Fourth", inventory)
        self.assertNotIn("ReadMe", inventory)
        self.assertTrue(inventory["Second"][0].nested)
        self.assertTrue(inventory["Third"][0].nested)

    def test_preserves_txt_and_addon_candidates(self) -> None:
        with TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            addon = root / "Example"
            addon.mkdir()
            for suffix in (".txt", ".addon"):
                (addon / f"Example{suffix}").write_text(
                    "## Title: Example\n## AddOnVersion: 10\n", encoding="utf-8"
                )
            inventory = build_inventory(root)

        self.assertEqual(len(inventory["Example"]), 2)

    def test_missing_addons_directory_raises(self) -> None:
        with TemporaryDirectory() as temp_dir:
            with self.assertRaises(NotADirectoryError):
                build_inventory(Path(temp_dir) / "missing")


if __name__ == "__main__":
    unittest.main()
