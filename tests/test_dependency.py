from pathlib import Path
import unittest

from addon_doctor.dependency import (
    DependencyStatus,
    diagnose_inventory,
    diagnose_manifest_dependencies,
)
from addon_doctor.inventory import InventoryEntry
from addon_doctor.manifest import AddonManifest, Dependency


def manifest(
    addon_id: str,
    *,
    addon_version: int | None = None,
    dependencies: tuple[Dependency, ...] = (),
    pc_dependencies: tuple[Dependency, ...] = (),
    console_dependencies: tuple[Dependency, ...] = (),
    optional_dependencies: tuple[Dependency, ...] = (),
) -> AddonManifest:
    return AddonManifest(
        path=Path(f"{addon_id}/{addon_id}.txt"),
        addon_id=addon_id,
        title=addon_id,
        author=None,
        version=None,
        addon_version=addon_version,
        api_versions=(),
        is_library=False,
        dependencies=dependencies,
        pc_dependencies=pc_dependencies,
        console_dependencies=console_dependencies,
        optional_dependencies=optional_dependencies,
    )


def entry(value: AddonManifest) -> InventoryEntry:
    return InventoryEntry(
        manifest=value,
        relative_path=value.path,
        top_level_directory=value.addon_id,
        nested=False,
    )


class DependencyTests(unittest.TestCase):
    def test_pc_hard_dependencies_and_versions(self) -> None:
        owner = manifest(
            "Owner",
            dependencies=(Dependency("LibA", 20), Dependency("Missing")),
            pc_dependencies=(Dependency("LibPC", 5),),
            console_dependencies=(Dependency("LibConsole", 1),),
        )
        inventory = {
            "LibA": (entry(manifest("LibA", addon_version=19)),),
            "LibPC": (entry(manifest("LibPC", addon_version=5)),),
        }

        results = diagnose_manifest_dependencies(owner, inventory)
        statuses = {result.dependency.name: result.status for result in results}

        self.assertEqual(statuses["LibA"], DependencyStatus.VERSION_TOO_OLD)
        self.assertEqual(statuses["Missing"], DependencyStatus.MISSING)
        self.assertEqual(statuses["LibPC"], DependencyStatus.OK)
        self.assertNotIn("LibConsole", statuses)

    def test_unknown_version_is_not_reported_as_too_old(self) -> None:
        owner = manifest("Owner", dependencies=(Dependency("LibA", 20),))
        inventory = {"LibA": (entry(manifest("LibA")),)}
        result = diagnose_manifest_dependencies(owner, inventory)[0]
        self.assertEqual(result.status, DependencyStatus.VERSION_UNKNOWN)

    def test_any_known_candidate_can_satisfy_minimum(self) -> None:
        owner = manifest("Owner", dependencies=(Dependency("LibA", 20),))
        inventory = {
            "LibA": (
                entry(manifest("LibA", addon_version=10)),
                entry(manifest("LibA", addon_version=25)),
            )
        }
        result = diagnose_manifest_dependencies(owner, inventory)[0]
        self.assertEqual(result.status, DependencyStatus.OK)
        self.assertEqual(result.installed_versions, (10, 25))

    def test_optional_missing_is_warning_only(self) -> None:
        owner = manifest(
            "Owner", optional_dependencies=(Dependency("OptionalLib", 99),)
        )
        result = diagnose_manifest_dependencies(owner, {})[0]
        self.assertEqual(result.status, DependencyStatus.OPTIONAL_MISSING)
        self.assertTrue(result.optional)

    def test_duplicate_manifest_candidates_do_not_duplicate_identical_findings(self) -> None:
        first = manifest(
            "Owner",
            addon_version=1,
            optional_dependencies=(Dependency("OptionalLib"),),
        )
        second = manifest(
            "Owner",
            addon_version=2,
            optional_dependencies=(Dependency("OptionalLib"),),
        )
        inventory = {"Owner": (entry(first), entry(second))}

        results = diagnose_inventory(inventory)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, DependencyStatus.OPTIONAL_MISSING)


if __name__ == "__main__":
    unittest.main()
