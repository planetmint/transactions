# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.8.0] - 2023-03-29
### Added
- Script class for zenroom script validation
- adjusted script schema validation

## [0.7.1] - 2023-03-06
### Changed
- renamed constants on Transaction class

## [0.7.0] - 2023-02-14
### Fixed
- Inconsistent TX validation: made it consistent.

## [0.6.0] - 2022-01-26
### Added
- Transactional types: Compose and Decompose
- structural tests for Transaction class

## [0.5.0] - 2022-12-12
### Fixed
- renamed method from _simple_ to _ed25519_ (a more expressive and speaking name)
- added planetmint-cryptocondition dependency to 1.1.0 avoiding the "keyring" inconsistency of zenroom contracts (sign vs. execute)
- simplified package management by merging test-group into dev-group

## [0.4.1] - 2022-12-12
### Fixed
- fixed a naming collision within the transaction class that lead to an recursive call

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

