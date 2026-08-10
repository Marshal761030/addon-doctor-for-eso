"""Dependency diagnostics for ESO add-ons."""

from dataclasses import dataclass
from enum import Enum
from typing import Iterable

from .inventory import InventoryEntry
from .manifest import AddonManifest, Dependency


class DependencyStatus(str, Enum):
    """Result of checking one manifest dependency."""

    OK = "OK"
    MISSING = "MISSING"
    VERSION_TOO_OLD = "VERSION_TOO_OLD"
    VERSION_UNKNOWN = "VERSION_UNKNOWN"
    OPTIONAL_MISSING = "OPTIONAL_MISSING"


@dataclass(frozen=True)
class DependencyResult:
    """Diagnostic result for one dependency."""

    owner_id: str
    dependency: Dependency
    status: DependencyStatus
    optional: bool
    installed_versions: tuple[int, ...]


def _known_versions(entries: Iterable[InventoryEntry]) -> tuple[int, ...]:
    return tuple(
        sorted(
            {
                entry.manifest.addon_version
                for entry in entries
                if entry.manifest.addon_version is not None
            }
        )
    )


def _check_one(
    owner_id: str,
    dependency: Dependency,
    inventory: dict[str, tuple[InventoryEntry, ...]],
    *,
    optional: bool,
) -> DependencyResult:
    entries = inventory.get(dependency.name, ())

    if not entries:
        return DependencyResult(
            owner_id=owner_id,
            dependency=dependency,
            status=(
                DependencyStatus.OPTIONAL_MISSING
                if optional
                else DependencyStatus.MISSING
            ),
            optional=optional,
            installed_versions=(),
        )

    versions = _known_versions(entries)

    if dependency.minimum_version is None or optional:
        return DependencyResult(
            owner_id=owner_id,
            dependency=dependency,
            status=DependencyStatus.OK,
            optional=optional,
            installed_versions=versions,
        )

    if not versions:
        status = DependencyStatus.VERSION_UNKNOWN
    elif max(versions) < dependency.minimum_version:
        status = DependencyStatus.VERSION_TOO_OLD
    else:
        status = DependencyStatus.OK

    return DependencyResult(
        owner_id=owner_id,
        dependency=dependency,
        status=status,
        optional=optional,
        installed_versions=versions,
    )


def diagnose_manifest_dependencies(
    manifest: AddonManifest,
    inventory: dict[str, tuple[InventoryEntry, ...]],
) -> tuple[DependencyResult, ...]:
    """Diagnose PC dependencies for one manifest.

    PC diagnostics include DependsOn and PCDependsOn. ConsoleDependsOn is not
    evaluated on PC. OptionalDependsOn is reported separately and never becomes
    a hard failure.
    """
    results: list[DependencyResult] = []

    for dependency in (*manifest.dependencies, *manifest.pc_dependencies):
        results.append(
            _check_one(
                manifest.addon_id,
                dependency,
                inventory,
                optional=False,
            )
        )

    for dependency in manifest.optional_dependencies:
        results.append(
            _check_one(
                manifest.addon_id,
                dependency,
                inventory,
                optional=True,
            )
        )

    return tuple(results)


def diagnose_inventory(
    inventory: dict[str, tuple[InventoryEntry, ...]],
) -> tuple[DependencyResult, ...]:
    """Diagnose dependencies while suppressing duplicate identical findings."""
    results: list[DependencyResult] = []
    seen: set[DependencyResult] = set()

    for entries in inventory.values():
        for entry in entries:
            for result in diagnose_manifest_dependencies(entry.manifest, inventory):
                if result in seen:
                    continue
                seen.add(result)
                results.append(result)

    return tuple(results)
