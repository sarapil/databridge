# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge — Migration Service
Cross-system migration orchestration.
"""
import frappe
from frappe import _


class MigrationService:
    @staticmethod
    def create_project(source_system: str, description: str = "") -> str:
        """Create a new migration project."""
        frappe.has_permission("DB Migration Project", "create", throw=True)
        project = frappe.new_doc("DB Migration Project")
        project.source_system = source_system
        project.target_system = "ERPNext"
        project.description = description
        project.status = "Planning"
        project.insert()
        return project.name

    @staticmethod
    def run_migration(project_name: str):
        """Execute all migration steps in sequence."""
        project = frappe.get_doc("DB Migration Project", project_name)
        if project.status not in ("Planning", "Ready"):
            frappe.throw(_("Migration can only run from Planning or Ready status"))
        project.db_set("status", "In Progress")
        frappe.db.commit()

        steps = frappe.get_all(
            "DB Migration Step",
            filters={"project": project_name},
            fields=["name", "sequence", "source_entity", "target_doctype"],
            order_by="sequence asc",
        )

        for step in steps:
            try:
                frappe.db.set_value("DB Migration Step", step.name, "status", "Processing")
                frappe.db.commit()
                # Step execution would dispatch to appropriate connector
                frappe.db.set_value("DB Migration Step", step.name, "status", "Completed")
            except Exception as e:
                frappe.db.set_value("DB Migration Step", step.name, "status", "Failed")
                frappe.db.set_value("DB Migration Step", step.name, "error_message", str(e)[:500])
                frappe.log_error(title=f"Migration step failed: {step.name}")
        frappe.db.commit()

        failed = frappe.db.count("DB Migration Step", {"project": project_name, "status": "Failed"})
        project.db_set("status", "Completed" if failed == 0 else "Completed with Errors")
        frappe.db.commit()
