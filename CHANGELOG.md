# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.0] - 2022-12-09
### Added
- support to validate v2.0 and v3.0 transaction schemes

## [0.3.0] - 2022-12-02
### Added
- added delegated signing support (callback calling)

## [0.2.2] - 2022-11-28
### Fixed
- fixed: upgraded to planetmint-cryptoconditions version 1.0.0

## [0.2.1] - 2022-11-14
### Fixed
- fixed `Create` assets validation according to transactions spec `v3.0`

### Removed
- removed unused code dependent on a `localmongodb` backend

## [0.2.0] - 2022-10-27
### Changed
- update transaction version number from `v2.0` to `v3.0`
- adjusted `Transaction`, `Create`, `Transfer`, `Election`, `ValidatorElection`, `Vote` assets usage
- adjusted test suite for transaction spec `v3.0` 

### Fixed
- fixed `assets` and `output.condition` on `v3.0` yaml files

## [0.1.0] - 2022-10-10
### Added
- [planetmint](https://github.com/planetmint/planetmint) transactions module
- initial `pyproject.toml` and `poetry.lock`

