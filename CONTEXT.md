# DataBridge — AI Context
# سياق الذكاء الاصطناعي — جسر البيانات

## What is DataBridge?

DataBridge is a data integration platform for Frappe/ERPNext. It handles import, export, migration, and real-time synchronization between Frappe and external systems through configurable connectors and field mapping.

## Architecture

- **21 DocTypes** across 8 modules
- **6 Services**: import, migration, sync, mapping, validation, history
- **5 Roles**: DB Admin, DB Manager, DB Operator, DB Viewer, DB API User
- **14 CAPS Capabilities**: DB_manage_settings through DB_manage_api_hub

## Key DocTypes

- `DB Settings` — Global configuration
- `DB Source Connection` — External system connections
- `DB Field Map` — Source-to-target field mapping
- `DB Import Job` — Import execution and tracking
- `DB Export Job` — Export execution and tracking
- `DB Sync Schedule` — Recurring sync configuration
- `DB Migration Plan` — Multi-step migration orchestration
- `DB Validation Rule` — Data quality rules

## Dependencies

`frappe`, `frappe_visual`, `arkan_help`, `base_base`

## Tech Stack

Python 3.14+ | Frappe v16 | MariaDB 11.8+ | Node.js v24+
