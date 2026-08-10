"""Human-readable local diagnostic reports."""

from collections import Counter
from pathlib import Path

from .dependency import DependencyResult, DependencyStatus, diagnose_inventory
from .inventory import InventoryEntry, build_inventory


def _format_versions(result: DependencyResult) -> str:
    if not result.installed_versions:
        return "unknown"
    return ", ".join(str(value) for value in result.installed_versions)


def build_text_report(addons_dir: Path) -> str:
    """Build a local text report without writing or uploading any data."""
    inventory = build_inventory(addons_dir)
    results = diagnose_inventory(inventory)
    duplicates = {addon_id: entries for addon_id, entries in inventory.items() if len(entries) > 1}
    status_counts = Counter(result.status for result in results)

    lines: list[str] = [
        "Addon Doctor for ESO - Local Diagnostic Report",
        "=" * 46,
        f"AddOns directory: {addons_dir}",
        f"Unique add-on/library IDs: {len(inventory)}",
        f"Manifest candidates: {sum(len(entries) for entries in inventory.values())}",
        f"IDs with multiple manifest candidates: {len(duplicates)}",
        "",
        "Dependency summary",
        "------------------",
    ]

    for status in DependencyStatus:
        lines.append(f"{status.value}: {status_counts.get(status, 0)}")

    problem_results = tuple(
        result for result in results if result.status is not DependencyStatus.OK
    )

    lines.extend(["", "Dependency findings", "-------------------"])
    if not problem_results:
        lines.append("No dependency problems detected.")
    else:
        for result in problem_results:
            required = (
                f">={result.dependency.minimum_version}"
                if result.dependency.minimum_version is not None
                else ""
            )
            suffix = ""
            if result.status in {
                DependencyStatus.VERSION_TOO_OLD,
                DependencyStatus.VERSION_UNKNOWN,
            }:
                suffix = f"; installed AddOnVersion: {_format_versions(result)}"

            lines.append(
                f"[{result.status.value}] {result.owner_id}: "
                f"{result.dependency.name}{required}{suffix}"
            )

    lines.extend(["", "Multiple manifest candidates", "----------------------------"])
    if not duplicates:
        lines.append("None detected.")
    else:
        for addon_id, entries in duplicates.items():
            lines.append(f"{addon_id}:")
            for entry in entries:
                version = entry.manifest.addon_version
                lines.append(
                    f"  - {entry.relative_path} (AddOnVersion: "
                    f"{version if version is not None else 'unknown'})"
                )

    lines.extend(
        [
            "",
            "Privacy",
            "-------",
            "This report is generated locally. Addon Doctor does not upload it.",
        ]
    )

    return "\n".join(lines) + "\n"
