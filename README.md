# Addon Doctor for ESO

A privacy-focused local diagnostic tool for The Elder Scrolls Online add-ons.

## Status

Early development / experimental.

The project is currently being designed and tested. No stable release is available yet.

## Goal

Addon Doctor for ESO aims to help players diagnose common add-on installation and dependency problems without modifying the game client.

Planned v0.1 features:

- Detect the local ESO AddOns directory
- Scan installed add-ons
- Read add-on manifest information
- Detect missing or unresolved library dependencies
- Identify common installation problems
- Generate a local diagnostic report

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

The initial version is designed as a read-only diagnostic utility.

Users should always keep backups of important game configuration files before using experimental software.

## Disclaimer

This is an independent open-source community project.

It is not affiliated with, endorsed by, or sponsored by ZeniMax Online Studios, Bethesda Softworks, Microsoft, or The Elder Scrolls Online.

The Elder Scrolls Online and related trademarks belong to their respective owners.

## License

Licensed under the MIT License.
