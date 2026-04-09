# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""
DataBridge — Demo Data
Load / clear demo data for showcasing app features.
"""
import frappe
from frappe import _


def load_demo_data():
    """Load realistic demo records for DataBridge."""
    if frappe.flags.in_install or frappe.flags.in_migrate:
        return

    # Demo source connections
    connections = [
        {"connection_name": "Demo CSV Source", "source_type": "CSV", "enabled": 1},
        {"connection_name": "Demo API Source", "source_type": "REST API", "enabled": 1},
        {"connection_name": "Demo Database Source", "source_type": "Database", "enabled": 0},
    ]
    for conn in connections:
        if not frappe.db.exists("DB Source Connection", {"connection_name": conn["connection_name"]}):
            doc = frappe.get_doc({"doctype": "DB Source Connection", **conn})
            doc.insert(ignore_permissions=True)

    # Demo field maps
    maps = [
        {
            "map_name": "Customer Import Map",
            "target_doctype": "Customer",
            "enabled": 1,
        },
        {
            "map_name": "Item Import Map",
            "target_doctype": "Item",
            "enabled": 1,
        },
    ]
    for m in maps:
        if not frappe.db.exists("DB Field Map", {"map_name": m["map_name"]}):
            doc = frappe.get_doc({"doctype": "DB Field Map", **m})
            doc.insert(ignore_permissions=True)

    # Demo import jobs
    jobs = [
        {"job_name": "Demo Customer Import", "target_doctype": "Customer", "status": "Completed",
         "total_records": 150, "success_count": 148, "error_count": 2},
        {"job_name": "Demo Item Import", "target_doctype": "Item", "status": "Completed",
         "total_records": 500, "success_count": 500, "error_count": 0},
        {"job_name": "Demo Failed Import", "target_doctype": "Supplier", "status": "Failed",
         "total_records": 50, "success_count": 0, "error_count": 50},
    ]
    for job in jobs:
        if not frappe.db.exists("DB Import Job", {"job_name": job["job_name"]}):
            doc = frappe.get_doc({"doctype": "DB Import Job", **job})
            doc.insert(ignore_permissions=True)

    # Demo validation rules
    rules = [
        {"rule_name": "Customer Name Required", "target_doctype": "Customer",
         "field_name": "customer_name", "validation_type": "Required", "enabled": 1},
        {"rule_name": "Email Format Check", "target_doctype": "Customer",
         "field_name": "email_id", "validation_type": "Format", "enabled": 1},
    ]
    for rule in rules:
        if not frappe.db.exists("DB Validation Rule", {"rule_name": rule["rule_name"]}):
            doc = frappe.get_doc({"doctype": "DB Validation Rule", **rule})
            doc.insert(ignore_permissions=True)

    frappe.db.commit()
    frappe.msgprint(_("DataBridge demo data loaded successfully."))


def clear_demo_data():
    """Remove all demo data."""
    for dt in ["DB Import Job", "DB Validation Rule", "DB Field Map", "DB Source Connection"]:
        for name in frappe.get_all(dt, filters={"owner": "Administrator"}, pluck="name", limit=50):
            try:
                frappe.delete_doc(dt, name, force=True)
            except Exception:
                pass
    frappe.db.commit()
    frappe.msgprint(_("DataBridge demo data cleared."))
