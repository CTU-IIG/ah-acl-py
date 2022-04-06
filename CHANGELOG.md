# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/).

## Unreleased
## 0.1.0 - 2022-04-05
### Added
- `ArrowheadInterface`
  - New class for configurating used interface.
- `ArrowheadService`
  - Now also contain ID, timestamp of creation and timestamp of last update.
- `ArrowheadSystem`
  - Now also contain ID, timestamp of creation and timestamp of last update.
  - New attribute `interfaces` that holds all available `ArrowheadInterface`.
- `Error` class for storing the data about Arrowhead Core error.
- Automatically build Wagon archives for 'x86_64', 'aarch64' and 'armv7l'.
- IDs and timestamps are automatically updated after receiving a response from Arrowhead Core.

### Changed
- Errors are no longer automatically printed out.
- Received IDs are no longer automatically printed out.
- Updated readme.

### Fixed
- Public keys can be stored on oneline inside the file.

## 0.0.1 - 2022-04-04
### Added
- First draft version of the library.
