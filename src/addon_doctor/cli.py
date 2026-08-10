"""Command-line interface for Addon Doctor for ESO."""

from argparse import ArgumentParser
from pathlib import Path
import sys

from .paths import detect_addons_directory
from .report import build_text_report


def _parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="addon-doctor-for-eso",
        description="Read-only local diagnostics for ESO add-ons.",
    )
    parser.add_argument(
        "addons_dir",
        nargs="?",
        type=Path,
        help="Path to the ESO live/AddOns directory. Auto-detected when omitted.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    addons_dir = args.addons_dir or detect_addons_directory()

    if addons_dir is None:
        print(
            "ESO AddOns directory was not found automatically. "
            "Pass the path explicitly.",
            file=sys.stderr,
        )
        return 2

    try:
        report = build_text_report(addons_dir)
    except (FileNotFoundError, NotADirectoryError, OSError) as exc:
        print(f"Scan failed: {exc}", file=sys.stderr)
        return 2

    print(report, end="")
    return 0
