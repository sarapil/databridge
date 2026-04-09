# DataBridge — Threat Model

## Overview

Security analysis for DataBridge data migration and integration platform.

## Assets

| Asset | Sensitivity | Description |
|-------|------------|-------------|
| DB Source Connection credentials | HIGH | Database passwords, API keys, FTP credentials |
| Imported data | MEDIUM-HIGH | May contain PII, financial data |
| DB API Keys | HIGH | External API access tokens |
| Migration plans | LOW | Operational metadata |

## Threats (OWASP-aligned)

### T1: SQL Injection via Dynamic Queries
- **Risk**: Source queries could inject SQL into target database
- **Mitigation**: All queries use parameterized statements via `frappe.db.sql(... %(param)s ...)`
- **Status**: Mitigated

### T2: Credential Exposure in Connections
- **Risk**: Database passwords and API keys stored insecurely
- **Mitigation**: Credentials stored in Password field type (encrypted at rest)
- **Status**: Mitigated

### T3: Data Exfiltration via Export
- **Risk**: Unauthorized user exports sensitive data
- **Mitigation**: CAPS capability `DB_export_data` required, all exports logged in DB Data Audit
- **Status**: Mitigated

### T4: Unauthorized External API Access
- **Risk**: API Hub endpoints accessed without authentication
- **Mitigation**: DB API Key required for all external calls, keys rotatable
- **Status**: Mitigated

### T5: Data Corruption via Bad Import
- **Risk**: Invalid data imported corrupts production records
- **Mitigation**: DB Validation Rule engine validates all rows before insert, rollback on failure
- **Status**: Mitigated

## Audit Logging

- All imports/exports logged in DB Data Audit with user, timestamp, row counts
- API calls logged in DB API Log
- Sync activity logged in DB Sync Log
