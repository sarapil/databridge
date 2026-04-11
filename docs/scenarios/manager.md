# DB Manager — Usage Scenarios

# سيناريوهات استخدام — مدير الترحيل

## Role Overview

- **Title**: Migration Manager / مدير الترحيل
- **CAPS Capabilities**: DB_run_migrations, DB_manage_mappings, DB_manage_sync, DB_view_audit, DB_view_history
- **Primary DocTypes**: DB Migration Plan, DB Field Map, DB Sync Profile
- **Device**: Desktop

## Daily Scenarios (يومي)

### DS-001: Create Field Mapping

- **Goal**: Map source fields to target ERPNext fields
- **Steps**:
  1. Navigate to Mapping workspace → DB Field Map → New
  2. Set target_doctype, use auto-map or manual field pairing
  3. Add transform rules if needed
  4. Save and test with sample data

### DS-002: Plan Data Migration

- **Goal**: Create a sequenced migration plan
- **Steps**:
  1. Navigate to Migration workspace → DB Migration Plan → New
  2. Add migration steps with dependency ordering
  3. Assign field maps to each step
  4. Review plan and execute

## Weekly Scenarios (أسبوعي)

### WS-001: Monitor Sync Profiles

- **Goal**: Ensure bidirectional syncs are running correctly
- **Steps**:
  1. Navigate to Sync workspace
  2. Review DB Sync Log for recent activity
  3. Resolve any DB Sync Conflict entries
