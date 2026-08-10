"""Helpers for locating common ESO AddOns directories on Windows."""

from pathlib import Path
import os


def candidate_addons_directories() -> tuple[Path, ...]:
    """Return common Windows ESO AddOns locations, without touching them."""
    candidates: list[Path] = []
    user_profile = os.environ.get("USERPROFILE")
    one_drive = os.environ.get("OneDrive")

    if user_profile:
        candidates.append(
            Path(user_profile)
            / "Documents"
            / "Elder Scrolls Online"
            / "live"
            / "AddOns"
        )

    if one_drive:
        candidates.append(
            Path(one_drive)
            / "Documents"
            / "Elder Scrolls Online"
            / "live"
            / "AddOns"
        )

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate).casefold()
        if key not in seen:
            seen.add(key)
            unique.append(candidate)

    return tuple(unique)


def detect_addons_directory() -> Path | None:
    """Return the first common ESO AddOns directory that exists."""
    for candidate in candidate_addons_directories():
        if candidate.is_dir():
            return candidate
    return None
