# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from databridge.api.response import success, error


@frappe.whitelist()
def start_migration(project_name):
    """Start a migration project execution."""
    frappe.has_permission("DB Migration Project", "write", throw=True)
    from databridge.services.migration_service import MigrationService
    try:
        frappe.enqueue(
            "databridge.services.migration_service.MigrationService.execute_migration",
            queue="long",
            timeout=1200,
            project_name=project_name,
        )
        return success(data={"project": project_name, "status": "Queued"}, message="Migration started")
    except Exception as e:
        frappe.log_error("DataBridge Migration Error")
        return error(str(e), error_code="DB_MIGRATION_FAILED")


@frappe.whitelist()
def rollback(rollback_point_name):
    """Rollback to a specific point."""
    frappe.has_permission("DB Rollback Point", "write", throw=True)
    from databridge.services.migration_service import MigrationService
    try:
        result = MigrationService.rollback_to(rollback_point_name)
        return success(data=result, message="Rollback completed")
    except Exception as e:
        frappe.log_error("DataBridge Rollback Error")
        return error(str(e), error_code="DB_ROLLBACK_FAILED")


@frappe.whitelist()
def trigger_sync(config_name):
    """Manually trigger a sync configuration."""
    frappe.has_permission("DB Sync Configuration", "write", throw=True)
    from databridge.services.sync_service import SyncService
    try:
        frappe.enqueue(
            "databridge.services.sync_service.SyncService.execute_sync",
            queue="default",
            timeout=300,
            config_name=config_name,
        )
        return success(data={"config": config_name, "status": "Queued"}, message="Sync triggered")
    except Exception as e:
        return error(str(e), error_code="DB_SYNC_FAILED")


@frappe.whitelist()
def get_sync_conflicts(config_name=None):
    """Get unresolved sync conflicts."""
    frappe.has_permission("DB Sync Conflict", "read", throw=True)
    filters = {"status": "Unresolved"}
    if config_name:
        filters["sync_configuration"] = config_name
    conflicts = frappe.get_all("DB Sync Conflict",
        filters=filters,
        fields=["name", "sync_configuration", "doctype", "document_name", "conflict_type", "creation"],
        order_by="creation desc",
        limit=50,
    )
    return success(data=conflicts)


@frappe.whitelist()
def get_connections():
    """List all configured source connections."""
    frappe.has_permission("DB Source Connection", "read", throw=True)
    connections = frappe.get_all("DB Source Connection",
        fields=["name", "connection_name", "connection_type", "enabled", "last_sync"],
        order_by="connection_name asc",
    )
    return success(data=connections)
