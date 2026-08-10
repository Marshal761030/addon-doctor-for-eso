# Changelog

All notable changes to Addon Doctor for ESO will be documented in this file.

## 0.1.0 - 2026-08-11

First usable alpha release.

### Added

- Read-only ESO AddOns directory scanning
- `.txt` and `.addon` manifest parsing
- Add-on and library inventory discovery
- Nested manifest discovery within the supported scan window
- Duplicate manifest candidate reporting
- PC dependency diagnostics for `DependsOn` and `PCDependsOn`
- Missing hard dependency detection
- Minimum `AddOnVersion` checking
- Separate optional dependency warnings
- Windows AddOns path auto-detection
- Local human-readable diagnostic report
- Command-line entry point
- Automated unit test suite
- GitHub Actions test workflow

### Privacy and safety

- No telemetry
- No diagnostic uploads
- No game-process memory scanning
- No DLL injection
- No account or Steam credential access
- No automatic modification, deletion, repair, or download of ESO add-ons
