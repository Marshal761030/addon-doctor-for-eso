# Addon Doctor for ESO v0.1.0

This is the first usable alpha release of Addon Doctor for ESO, a privacy-focused local diagnostic tool for The Elder Scrolls Online add-ons on Windows.

## Included in this release

- Local, read-only AddOns scanning
- `.txt` and `.addon` manifest parsing
- Add-on/library inventory discovery
- PC hard-dependency checks
- Minimum `AddOnVersion` checks
- Optional dependency warnings
- Duplicate manifest candidate reporting
- Automatic detection of common Windows ESO AddOns paths
- Human-readable terminal report
- Automated tests

## Safety model

Addon Doctor does not modify ESO add-ons, access account credentials, scan game memory, inject code, upload diagnostics, or include telemetry.

## Requirements

- Windows
- Python 3.11+

## Quick start

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m addon_doctor
```

Or specify the AddOns directory explicitly:

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m addon_doctor "C:\Users\YourName\Documents\Elder Scrolls Online\live\AddOns"
```

## Known limitations

- Alpha release; diagnostic behavior may still need refinement on unusual add-on layouts
- No automatic repairs or downloads
- No GUI
- No standalone Windows executable yet
