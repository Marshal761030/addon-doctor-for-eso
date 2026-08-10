from pathlib import Path
import tempfile
import unittest

from addon_doctor.manifest import parse_manifest


class ManifestParserTests(unittest.TestCase):
    def test_parses_metadata_and_dependencies(self):
        content = """## Title: Example AddOn
## Author: Tester
## Version: 1.2.3
## AddOnVersion: 123
## APIVersion: 101048 101050
## DependsOn: LibOne>=38 LibTwo
## OptionalDependsOn: LibOptional>=7
main.lua
"""

        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "Example.txt"
            path.write_text(content, encoding="utf-8")

            manifest = parse_manifest(path)

        self.assertEqual(manifest.title, "Example AddOn")
        self.assertEqual(manifest.author, "Tester")
        self.assertEqual(manifest.version, "1.2.3")
        self.assertEqual(manifest.addon_version, 123)
        self.assertEqual(manifest.api_versions, (101048, 101050))

        self.assertEqual(
            [(item.name, item.minimum_version) for item in manifest.dependencies],
            [("LibOne", 38), ("LibTwo", None)],
        )
        self.assertEqual(
            [
                (item.name, item.minimum_version)
                for item in manifest.optional_dependencies
            ],
            [("LibOptional", 7)],
        )

    def test_missing_manifest_raises(self):
        with self.assertRaises(FileNotFoundError):
            parse_manifest(Path("this-file-does-not-exist.txt"))


if __name__ == "__main__":
    unittest.main()