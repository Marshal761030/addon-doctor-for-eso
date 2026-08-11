# Addon Doctor for ESO v0.1.1

This maintenance release hardens the first public alpha's Windows packaging
and command-line regression coverage. The diagnostic behavior and read-only
privacy model are unchanged from v0.1.0.

## Included in this release

- Seven regression tests for common command-line success and error paths
- Wheel builds on the Windows Python 3.11 through 3.14 test matrix
- Clean virtual-environment installation of the built wheel
- Post-install checks for `python -m addon_doctor` and the
  `addon-doctor-for-eso` console command
- Direct wheel installation instructions in the README

## Safety model

Addon Doctor does not modify ESO add-ons, access account credentials, scan
game memory, inject code, upload diagnostics, or include telemetry.

## Requirements

- Windows
- Python 3.11+

## Install

Download `addon_doctor_for_eso-0.1.1-py3-none-any.whl`, open PowerShell in the
download directory, and run:

```powershell
py -m pip install .\addon_doctor_for_eso-0.1.1-py3-none-any.whl
```

Then run:

```powershell
addon-doctor-for-eso
```

## Known limitations

- Alpha release; unusual add-on layouts may still need refinement
- No automatic repairs or downloads
- No GUI
- No standalone Windows executable
