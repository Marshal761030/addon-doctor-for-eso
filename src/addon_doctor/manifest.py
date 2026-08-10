"""Parser for ESO add-on manifest files."""

from dataclasses import dataclass
from pathlib import Path
import re


_METADATA_RE = re.compile(r"^##\s*([^:]+):\s*(.*)$")
_DEPENDENCY_RE = re.compile(
    r"^(?P<name>[^>=\s]+)(?:>=(?P<minimum_version>\d+))?$"
)


@dataclass(frozen=True)
class Dependency:
    """An ESO add-on dependency."""

    name: str
    minimum_version: int | None = None


@dataclass(frozen=True)
class AddonManifest:
    """Relevant metadata parsed from an ESO add-on manifest."""

    path: Path
    title: str | None
    author: str | None
    version: str | None
    addon_version: int | None
    api_versions: tuple[int, ...]
    dependencies: tuple[Dependency, ...]
    optional_dependencies: tuple[Dependency, ...]


def _parse_dependencies(value: str) -> tuple[Dependency, ...]:
    dependencies: list[Dependency] = []

    for token in value.split():
        match = _DEPENDENCY_RE.fullmatch(token)
        if not match:
            continue

        minimum_version = match.group("minimum_version")

        dependencies.append(
            Dependency(
                name=match.group("name"),
                minimum_version=int(minimum_version)
                if minimum_version is not None
                else None,
            )
        )

    return tuple(dependencies)


def parse_manifest(path: Path) -> AddonManifest:
    """Read an ESO manifest without modifying it."""
    if not path.is_file():
        raise FileNotFoundError(f"Manifest not found: {path}")

    metadata: dict[str, str] = {}

    for line in path.read_text(
        encoding="utf-8-sig",
        errors="replace",
    ).splitlines():
        match = _METADATA_RE.match(line)
        if match:
            metadata[match.group(1).strip()] = match.group(2).strip()

    api_versions = tuple(
        int(value)
        for value in metadata.get("APIVersion", "").split()
        if value.isdigit()
    )

    addon_version_text = metadata.get("AddOnVersion")
    addon_version = (
        int(addon_version_text)
        if addon_version_text and addon_version_text.isdigit()
        else None
    )

    return AddonManifest(
        path=path,
        title=metadata.get("Title"),
        author=metadata.get("Author"),
        version=metadata.get("Version"),
        addon_version=addon_version,
        api_versions=api_versions,
        dependencies=_parse_dependencies(metadata.get("DependsOn", "")),
        optional_dependencies=_parse_dependencies(
            metadata.get("OptionalDependsOn", "")
        ),
    )