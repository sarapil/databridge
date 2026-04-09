# DB Operator — Usage Scenarios
# سيناريوهات استخدام — مشغل الاستيراد

## Role Overview

- **Title**: Import/Export Operator / مشغل الاستيراد والتصدير
- **CAPS Capabilities**: DB_import_data, DB_export_data, DB_view_history
- **Primary DocTypes**: DB Import Job, DB Export Job, DB Import Error
- **Device**: Desktop / Tablet

## Daily Scenarios (يومي)

### DS-001: Run CSV Import
- **Goal**: Import data from a CSV file into ERPNext
- **Steps**:
  1. Navigate to Import Export workspace → DB Import Job → New
  2. Set job_name, target_doctype, upload CSV file
  3. Select or create field mapping
  4. Start import and monitor progress
  5. Review DB Import Error for any failed rows

### DS-002: Export Data
- **Goal**: Export ERPNext data for external use
- **Steps**:
  1. Navigate to Import Export → DB Export Job → New
  2. Set source_doctype, filters, output format
  3. Execute export
  4. Download exported file

## Weekly Scenarios (أسبوعي)

### WS-001: Review Import History
- **Goal**: Check past import jobs for patterns
- **Steps**:
  1. Run Import History report
  2. Review success/error rates
  3. Flag recurring errors for admin attention
