<div align="center">

# 🔗 DataBridge

**Data Migration and Integration Hub for ERPNext**

[![CI](https://github.com/sarapil/databridge/actions/workflows/ci.yml/badge.svg)](https://github.com/sarapil/databridge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Overview

DataBridge is an enterprise data migration and integration platform for Frappe v16 / ERPNext. It provides a unified interface for importing data from CSV, REST APIs, databases, FTP/SFTP sources — with intelligent field mapping, validation rules, bidirectional sync, and full migration planning.

## Features

- **Multi-Source Connectors** — CSV, REST API, Database, FTP, SFTP with extensible connector framework
- **Intelligent Field Mapping** — Auto-mapping with confidence scoring, manual override, reusable map templates
- **Data Validation** — Required, format, unique, range, and custom validation rules per field
- **Migration Planner** — Dependency-aware migration sequencing with rollback support
- **Bidirectional Sync** — Scheduled sync with conflict detection and resolution strategies
- **Import/Export Engine** — Batch import with progress tracking, error logging, resume capability
- **API Hub** — Register and manage external API endpoints for data exchange
- **CAPS Integration** — 14 fine-grained capabilities for permission control
- **Bilingual** — Full Arabic + English support with RTL-ready UI

## Architecture

- **21 DocTypes** across 8 modules
- **6 Services**: import, migration, sync, mapping, validation, history
- **5 Roles**: DB Admin, DB Manager, DB Operator, DB Viewer, DB API User

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/sarapil/databridge --branch main
bench --site your-site install-app databridge
bench --site your-site migrate
```

### Required Apps

- `frappe` >= 16.0.0
- `frappe_visual` >= 0.1.0
- `arkan_help` >= 0.0.1
- `base_base` >= 0.0.1

## Configuration

1. Navigate to **DB Settings** and configure defaults
2. Set up source connections under **Connectors** workspace
3. Create field maps under **Mapping**
4. Define validation rules under **Data Integrity**

## Reports

| Report | Module | Description |
|--------|--------|-------------|
| Import History | Data Integrity | Import job status with pie chart |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. This app uses `pre-commit` for code quality:

```bash
cd apps/databridge
pre-commit install
```

Tools: ruff, eslint, prettier, pyupgrade

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## License

MIT — See [license.txt](license.txt)
