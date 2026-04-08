# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge — History & Rollback Service
"""
import frappe


def cleanup_old_logs():
    """Daily: clean up old import logs beyond retention period."""
    if not frappe.db.exists("DocType", "DB Settings"):
        return
    settings = frappe.get_cached_doc("DB Settings")
    retention_days = getattr(settings, "log_retention_days", 90) or 90
    cutoff = frappe.utils.add_days(frappe.utils.today(), -retention_days)
    frappe.db.delete("DB Import Log", {"creation": ["<", cutoff]})
    frappe.db.commit()
