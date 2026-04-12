# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

app_name = "databridge"
app_title = "DataBridge"
app_publisher = "Arkan Lab"
app_description = "Data Migration and Integration Hub for ERPNext"
app_email = "dev@arkan.it.com"
app_license = "mit"
app_icon = "/assets/databridge/images/databridge_icon.svg"
app_color = "#0EA5E9"
app_logo_url = "/assets/databridge/images/databridge-logo.svg"

# Required Apps
required_apps = ["frappe", "frappe_visual", "arkan_help", "base_base"]

# Feature Registry (Open Core)
app_feature_registry = {
    "csv_import": "free",
    "excel_import": "free",
    "basic_export": "free",
    "field_mapping": "free",
    "data_validation": "free",
    "rollback": "free",
    "odoo_connector": "premium",
    "quickbooks_connector": "premium",
    "sage_connector": "premium",
    "tally_connector": "premium",
    "salesforce_connector": "premium",
    "database_connector": "premium",
    "bidirectional_sync": "premium",
    "ai_field_mapping": "premium",
    "api_hub": "premium",
    "scheduled_sync": "premium",
}

# Apps Screen
add_to_apps_screen = [
    {
        "name": "databridge",
        "logo": "/assets/databridge/images/databridge_icon.svg",
        "title": "DataBridge",
        "route": "/app/databridge",
        "has_permission": "databridge.api.permissions.has_app_permission",
    }
]

# Includes in <head>
# CODESPACES: app_include_css = ["/assets/databridge/css/databridge_combined.css"]
# CODESPACES: app_include_js = ["/assets/databridge/js/databridge_combined.js"]

# Installation
before_install = "databridge.install.before_install"
after_install = "databridge.install.after_install"
after_migrate = ["databridge.seed.seed_data"]
before_uninstall = "databridge.install.before_uninstall"

# Boot Session
boot_session = "databridge.boot.boot_session"

# Scheduled Tasks
scheduler_events = {
    "cron": {
        "*/5 * * * *": [
            "databridge.services.sync_service.process_scheduled_syncs",
        ],
    },
    "daily": [
        "databridge.services.history_service.cleanup_old_logs",
    ],
    "hourly": [
        "databridge.services.sync_service.check_sync_health",
    ],
}

# Fixtures
fixtures = [
    {"dt": "Role", "filters": [["name", "like", "DB%"]]},
    {"dt": "Workspace", "filters": [["module", "like", "Databridge%"]]},
    {"dt": "Desktop Icon", "filters": [["app", "=", "databridge"]]},
]

# Website Route Rules
website_route_rules = [
    {"from_route": "/databridge-about", "to_route": "databridge_about"},
    {"from_route": "/databridge-onboarding", "to_route": "databridge_onboarding"},
]

# Global Search
global_search_doctypes = {
    "Default": [
        {"doctype": "DB Import Job", "index": 1},
        {"doctype": "DB Migration Project", "index": 2},
        {"doctype": "DB Field Map", "index": 3},
        {"doctype": "DB Sync Configuration", "index": 4},
    ]
}

export_python_type_annotations = True

# CAPS Integration
caps_capabilities = [
    {"name": "DB_view_dashboard", "category": "Module", "description": "عرض لوحة التحكم"},
    {"name": "DB_manage_migrations", "category": "Module", "description": "إدارة الهجرة"},
    {"name": "DB_manage_imports", "category": "Module", "description": "إدارة الاستيراد"},
    {"name": "DB_manage_sync", "category": "Module", "description": "إدارة المزامنة"},
    {"name": "DB_manage_api", "category": "Module", "description": "إدارة API"},
    {"name": "DB_run_import", "category": "Action", "description": "تنفيذ استيراد"},
    {"name": "DB_run_migration", "category": "Action", "description": "تنفيذ هجرة"},
    {"name": "DB_rollback_import", "category": "Action", "description": "تراجع عن استيراد"},
    {"name": "DB_create_connection", "category": "Action", "description": "إنشاء اتصال"},
    {"name": "DB_configure_sync", "category": "Action", "description": "إعداد مزامنة"},
    {"name": "DB_view_credentials", "category": "Field", "description": "عرض بيانات الاعتماد"},
    {"name": "DB_export_reports", "category": "Report", "description": "تصدير التقارير"},
    {"name": "DB_view_migration_reports", "category": "Report", "description": "تقارير الهجرة"},
    {"name": "DB_view_sync_reports", "category": "Report", "description": "تقارير المزامنة"},
]

caps_field_maps = [
    {"capability": "DB_view_credentials", "doctype": "DB Source Connection", "field": "api_key", "behavior": "hide"},
    {"capability": "DB_view_credentials", "doctype": "DB API Connection", "field": "api_key", "behavior": "hide"},
]
