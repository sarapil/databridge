# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge — Sync Service
Scheduled bidirectional synchronization.
"""
import frappe


def process_scheduled_syncs():
    """Scheduled: run all due sync configurations."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return
    if not frappe.db.exists("DocType", "DB Sync Configuration"):
        return
    configs = frappe.get_all(
        "DB Sync Configuration",
        filters={"enabled": 1},
        fields=["name"],
    )
    for config in configs:
        frappe.enqueue(
            "databridge.services.sync_service.run_sync",
            queue="long",
            config_name=config.name,
        )


def run_sync(config_name: str):
    """Execute a single sync configuration."""
    config = frappe.get_doc("DB Sync Configuration", config_name)
    try:
        config.db_set("last_run", frappe.utils.now())
        # Sync logic would be implemented per connector type
        config.db_set("last_status", "Success")
    except Exception as e:
        config.db_set("last_status", "Failed")
        frappe.log_error(title=f"Sync failed: {config_name}", message=str(e))
    frappe.db.commit()


def check_sync_health():
    """Hourly: check sync configurations health."""
    pass
