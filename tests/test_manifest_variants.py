"""Tests for ESO manifest variants."""

from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from addon_doctor.manifest import Dependency, parse_manifest


class ManifestVariantTests(unittest.TestCase):
    def test_parses_addon_and_platform_dependencies(self) -> None:
        content = """\
## Title: Pretty Display Title
## Author: Tester
## Version: 2.0
## AddOnVersion: 0009030
## APIVersion: 101050 101051
## IsLibrary: true
## DependsOn: LibCore>=10
## PCDependsOn: LibPC>=20
## ConsoleDependsOn: LibConsole>=30
## OptionalDependsOn: LibOptional>=40
"""

        with TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "InternalAddonId.addon"
            path.write_text(content, encoding="utf-8")

            manifest = parse_manifest(path)

        self.assertEqual(manifest.addon_id, "InternalAddonId")
        self.assertEqual(manifest.title, "Pretty Display Title")
        self.assertEqual(manifest.addon_version, 9030)
        self.assertEqual(manifest.api_versions, (101050, 101051))
        self.assertTrue(manifest.is_library)
        self.assertEqual(manifest.dependencies, (Dependency("LibCore", 10),))
        self.assertEqual(manifest.pc_dependencies, (Dependency("LibPC", 20),))
        self.assertEqual(
            manifest.console_dependencies,
            (Dependency("LibConsole", 30),),
        )
        self.assertEqual(
            manifest.optional_dependencies,
            (Dependency("LibOptional", 40),),
        )


if __name__ == "__main__":
    unittest.main()
