"""Smoke-test the installed wheel without importing from the source tree."""

from pathlib import Path
from tempfile import TemporaryDirectory
import os
import subprocess
import sys


EXPECTED_VERSION = "0.1.1"


def _run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Command failed ({completed.returncode}): {command!r}\n"
            f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
        )
    return completed.stdout


def _console_entry_point() -> Path:
    scripts_dir = Path(sys.executable).parent
    suffix = ".exe" if os.name == "nt" else ""
    executable = scripts_dir / f"addon-doctor-for-eso{suffix}"
    if not executable.is_file():
        raise FileNotFoundError(f"Console entry point not found: {executable}")
    return executable


def main() -> int:
    from addon_doctor import __version__

    if __version__ != EXPECTED_VERSION:
        raise RuntimeError(
            f"Installed version is {__version__!r}; expected {EXPECTED_VERSION!r}"
        )

    with TemporaryDirectory() as temp_dir:
        addons_dir = Path(temp_dir) / "AddOns"
        addon_dir = addons_dir / "SmokeTestAddon"
        addon_dir.mkdir(parents=True)
        (addon_dir / "SmokeTestAddon.txt").write_text(
            "## Title: Smoke Test AddOn\n## APIVersion: 101050\n",
            encoding="utf-8",
        )

        module_output = _run(
            [sys.executable, "-B", "-m", "addon_doctor", str(addons_dir)]
        )
        console_output = _run([str(_console_entry_point()), str(addons_dir)])

    for output in (module_output, console_output):
        if "Unique add-on/library IDs: 1" not in output:
            raise RuntimeError(f"Unexpected diagnostic output:\n{output}")

    print("Installed wheel smoke test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
