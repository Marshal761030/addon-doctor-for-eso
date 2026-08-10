"""Read-only inventory discovery for ESO add-on manifests."""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from .manifest import AddonManifest, parse_manifest


_MANIFEST_SUFFIXES = (".addon", ".txt")
_MAX_MANIFEST_DIRECTORY_DEPTH = 3


@dataclass(frozen=True)
class InventoryEntry:
    """A discovered ESO manifest candidate."""

    manifest: AddonManifest
    relative_path: Path
    top_level_directory: str
    nested: bool


def _matching_manifests(directory: Path) -> tuple[Path, ...]:
    """Return supported same-name manifest files directly in *directory*."""
    paths: list[Path] = []

    for suffix in _MANIFEST_SUFFIXES:
        candidate = directory / f"{directory.name}{suffix}"
        if candidate.is_file():
            paths.append(candidate)

    return tuple(paths)


def _walk_manifest_directories(
    directory: Path,
    *,
    depth: int,
) -> tuple[Path, ...]:
    """Return same-name manifests down to ESO's supported nested scan depth."""
    paths: list[Path] = list(_matching_manifests(directory))

    if depth >= _MAX_MANIFEST_DIRECTORY_DEPTH:
        return tuple(paths)

    children = sorted(
        (path for path in directory.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    )
    for child in children:
        paths.extend(_walk_manifest_directories(child, depth=depth + 1))

    return tuple(paths)


def find_manifest_paths(addons_dir: Path) -> tuple[Path, ...]:
    """Find manifests within ESO's documented nested folder scan window.

    The normal manifest lives at AddOns/<AddOn>/<AddOn>.<ext>. ESO's loader
    also searches two additional folder levels beneath that top-level add-on
    directory, allowing bundled/nested add-ons and libraries.
    """
    if not addons_dir.is_dir():
        raise NotADirectoryError(f"AddOns directory not found: {addons_dir}")

    paths: list[Path] = []
    top_level_directories = sorted(
        (path for path in addons_dir.iterdir() if path.is_dir()),
        key=lambda path: path.name.casefold(),
    )

    for directory in top_level_directories:
        paths.extend(_walk_manifest_directories(directory, depth=1))

    return tuple(paths)


def build_inventory(addons_dir: Path) -> dict[str, tuple[InventoryEntry, ...]]:
    """Build an add-on ID index while preserving duplicate manifest candidates."""
    grouped: defaultdict[str, list[InventoryEntry]] = defaultdict(list)

    for path in find_manifest_paths(addons_dir):
        manifest = parse_manifest(path)
        relative_path = path.relative_to(addons_dir)
        grouped[manifest.addon_id].append(
            InventoryEntry(
                manifest=manifest,
                relative_path=relative_path,
                top_level_directory=relative_path.parts[0],
                nested=len(relative_path.parts) > 2,
            )
        )

    return {
        addon_id: tuple(entries)
        for addon_id, entries in sorted(
            grouped.items(), key=lambda item: item[0].casefold()
        )
    }
