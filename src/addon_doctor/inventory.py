"""ESO add-on manifest inventory discovery."""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .manifest import AddonManifest, parse_manifest


_MANIFEST_SUFFIXES = {".txt", ".addon"}


@dataclass(frozen=True)
class InventoryEntry:
    """A manifest discovered within ESO's supported directory depth."""

    manifest: AddonManifest
    relative_path: Path
    top_level_directory: str
    embedded: bool


def _manifests_in_directory(directory: Path) -> tuple[Path, ...]:
    """Return same-name manifest files directly inside one directory."""
    result: list[Path] = []

    for path in directory.iterdir():
        if not path.is_file():
            continue

        if path.suffix.casefold() not in _MANIFEST_SUFFIXES:
            continue

        if path.stem.casefold() != directory.name.casefold():
            continue

        result.append(path)

    return tuple(sorted(result, key=lambda path: str(path).casefold()))


def find_manifest_paths(addons_dir: Path) -> tuple[Path, ...]:
    """Find manifests using ESO's two-directory-level discovery rule."""
    if not addons_dir.is_dir():
        raise NotADirectoryError(f"AddOns directory not found: {addons_dir}")

    paths: list[Path] = []

    level_one = sorted(
        (path for path in addons_dir.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    )

    for directory in level_one:
        paths.extend(_manifests_in_directory(directory))

        level_two = sorted(
            (path for path in directory.iterdir() if path.is_dir()),
            key=lambda path: path.name.casefold(),
        )

        for nested_directory in level_two:
            paths.extend(_manifests_in_directory(nested_directory))

    return tuple(paths)


def build_inventory(
    addons_dir: Path,
) -> dict[str, tuple[InventoryEntry, ...]]:
    """Build an ID index while preserving multiple manifest candidates."""
    grouped: defaultdict[str, list[InventoryEntry]] = defaultdict(list)

    for path in find_manifest_paths(addons_dir):
        manifest = parse_manifest(path)
        relative_path = path.relative_to(addons_dir)

        grouped[manifest.addon_id].append(
            InventoryEntry(
                manifest=manifest,
                relative_path=relative_path,
                top_level_directory=relative_path.parts[0],
                embedded=len(relative_path.parts) == 3,
            )
        )

    return {
        addon_id: tuple(entries)
        for addon_id, entries in sorted(
            grouped.items(),
            key=lambda item: item[0].casefold(),
        )
    }
