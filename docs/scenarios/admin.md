# DB Admin — Usage Scenarios
# سيناريوهات استخدام — مدير النظام

## Role Overview

- **Title**: DataBridge Administrator / مدير DataBridge
- **CAPS Capabilities**: DB_manage_settings, DB_manage_connections, DB_manage_api_hub, DB_manage_validation, DB_bulk_operations
- **Primary DocTypes**: DB Settings, DB Source Connection, DB API Endpoint, DB Validation Rule
- **Device**: Desktop

## Daily Scenarios (يومي)

### DS-001: Configure New Data Source
- **Goal**: Add a new external data source connection
- **Steps**:
  1. Navigate to Connectors workspace → DB Source Connection → New
  2. Set connection_name, source_type, credentials
  3. Test connection
  4. Verify: Connection status shows "Connected"

### DS-002: Create Validation Rules
- **Goal**: Define data quality rules for imports
- **Steps**:
  1. Navigate to Data Integrity → DB Validation Rule → New
  2. Set target_doctype, field_name, validation_type
  3. Enable rule
  4. Verify: Rule appears in active rules list

## Weekly Scenarios (أسبوعي)

### WS-001: Review Data Audit
- **Goal**: Check data integrity across recent imports
- **Steps**:
  1. Navigate to Data Integrity workspace
  2. Review DB Data Audit records
  3. Flag any anomalies for investigation

## Monthly Scenarios (شهري)

### MS-001: Review API Hub Usage
- **Goal**: Audit external API endpoint usage
- **Steps**:
  1. Navigate to Api Hub workspace
  2. Review DB API Log for usage patterns
  3. Rotate or revoke unused DB API Keys
