"""Read-only helpers for scanning an ESO AddOns directory."""

from pathlib import Path


def list_addon_directories(addons_dir: Path) -> list[str]:
    """Return installed add-on directory names without modifying any files."""
    if not addons_dir.is_dir():
        raise NotADirectoryError(f"AddOns directory not found: {addons_dir}")

    return sorted(
        (item.name for item in addons_dir.iterdir() if item.is_dir()),
        key=str.casefold,
    )
