# Addon Doctor for ESO

A privacy-focused local diagnostic tool for The Elder Scrolls Online add-ons.

## Status

Early development / experimental. The current development snapshot provides read-only scanning, manifest parsing, inventory discovery, dependency diagnostics, and a local text report.

## Goal

Addon Doctor for ESO helps players diagnose common add-on installation and dependency problems without modifying the game client.

Current v0.1 development features:

- Detect common Windows ESO AddOns locations, or accept a path manually
- Scan installed add-on manifest files using ESO's documented folder rules
- Read `.txt` and `.addon` manifest metadata
- Index add-ons and libraries, preserving duplicate manifest candidates
- Check `DependsOn` and `PCDependsOn` dependencies on PC
- Report missing dependencies and insufficient `AddOnVersion` values
- Report missing optional dependencies separately
- Generate a local human-readable diagnostic report

## Run

From the repository root:

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m addon_doctor
```

Or pass the AddOns path explicitly:

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m addon_doctor "C:\Users\YourName\Documents\Elder Scrolls Online\live\AddOns"
```

The program prints the report to the terminal. It does not write into the ESO AddOns directory.

## Tests

```powershell
$env:PYTHONPATH="$PWD\src"
py -B -m unittest discover -s tests -v
```

## Privacy

Privacy is a core design requirement.

The planned v0.1:

- Runs locally
- Does not require an ESO account or password
- Does not access Steam credentials
- Does not scan game process memory
- Does not inject code into the game
- Does not upload diagnostic data
- Does not include telemetry
- Uses read-only diagnostics by default

Sensitive user data will not be intentionally collected or published.

## Safety

The initial version is designed as a read-only diagnostic utility. It does not automatically delete, move, repair, download, or modify installed add-ons.

## Disclaimer

This is an independent open-source community project.

It is not affiliated with, endorsed by, or sponsored by ZeniMax Online Studios, Bethesda Softworks, Microsoft, or The Elder Scrolls Online.

The Elder Scrolls Online and related trademarks belong to their respective owners.

## License

Licensed under the MIT License.
