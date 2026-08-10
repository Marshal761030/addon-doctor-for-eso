# Addon Doctor for ESO

A privacy-focused local diagnostic tool for The Elder Scrolls Online add-ons.

## Status

**v0.1.0 (alpha)** — the first usable public release.

Addon Doctor currently provides read-only scanning, manifest parsing, add-on/library inventory discovery, dependency diagnostics, and a local text report.

## What it does

- Detects common Windows ESO `AddOns` locations, or accepts a path manually
- Scans ESO manifest files within the supported nested folder window
- Reads both `.txt` and `.addon` manifest metadata
- Indexes add-ons and libraries while preserving duplicate manifest candidates
- Checks PC `DependsOn` and `PCDependsOn` dependencies
- Reports missing hard dependencies
- Reports insufficient `AddOnVersion` values
- Reports missing optional dependencies separately as warnings
- Shows duplicate manifest candidates for manual review
- Generates the report locally in the terminal

## Privacy and safety

Addon Doctor is intentionally local and read-only.

It does **not**:

- Require an ESO account or password
- Access Steam credentials
- Scan ESO process memory
- Inject code into the game
- Delete, move, repair, download, or modify installed add-ons
- Upload diagnostic data
- Include telemetry

The current release reads add-on manifest files only for diagnostic purposes.

## Requirements

- Windows
- Python 3.11 or newer

## Run from the repository

Open PowerShell in the repository root:

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m addon_doctor
```

Addon Doctor will try to detect the ESO `live\AddOns` directory automatically.

You can also pass the directory explicitly:

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m addon_doctor "C:\Users\YourName\Documents\Elder Scrolls Online\live\AddOns"
```

The report is printed to the terminal. Addon Doctor does not write into the ESO `AddOns` directory.

## Install as a command-line tool

From the repository root:

```powershell
py -m pip install .
```

Then run:

```powershell
addon-doctor-for-eso
```

Or provide the AddOns path:

```powershell
addon-doctor-for-eso "C:\Users\YourName\Documents\Elder Scrolls Online\live\AddOns"
```

## Understanding the report

Dependency results include:

- `OK` — dependency is installed and any required `AddOnVersion` is satisfied
- `MISSING` — required dependency was not found
- `VERSION_TOO_OLD` — dependency exists but its known `AddOnVersion` is below the required minimum
- `VERSION_UNKNOWN` — a minimum version is required but no usable `AddOnVersion` is available
- `OPTIONAL_MISSING` — optional dependency is not installed; this is a warning, not a hard dependency failure

The report also lists add-on/library IDs that have multiple manifest candidates so unusual or legacy installations can be reviewed manually.

## Tests

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m unittest discover -s tests -v
```

## Current limitations

v0.1.0 is intentionally conservative:

- It diagnoses dependency state but does not repair anything automatically
- Duplicate manifest candidates are reported rather than automatically deleted or resolved
- Optional dependencies are informational only
- No GUI is included yet
- No executable (`.exe`) build is included yet

## Disclaimer

This is an independent open-source community project.

It is not affiliated with, endorsed by, or sponsored by ZeniMax Online Studios, Bethesda Softworks, Microsoft, or The Elder Scrolls Online.

The Elder Scrolls Online and related trademarks belong to their respective owners.

## License

Licensed under the MIT License.
