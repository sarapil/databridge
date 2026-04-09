# Changelog — DataBridge

All notable changes to DataBridge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] — 2024-01-01

### Added

- Initial release with 21 DocTypes across 8 modules
- Source connection management (CSV, REST API, Database, FTP, SFTP)
- Import/export engine with field mapping and validation
- Migration planner with dependency resolution
- Bidirectional sync with conflict detection
- Data integrity validation rules (Required, Format, Unique, Range, Custom)
- API Hub for external endpoint registration
- Connector framework for extensible data sources
- Import History script report with chart
- 6 services: import, migration, sync, mapping, validation, history
- CAPS capability integration (14 capabilities)
- Full Arabic translation (ar.csv, 293+ strings)
- Seed data for connections, field maps, and validation rules
- API v1 endpoints (import_export, mapping, migration)
- 6 workspace pages for desk navigation
- Unit and integration tests
- Demo data loader
- CI/CD workflows (ci, linters, release, auto-label, stale)
- GitHub wiki (9 pages)
