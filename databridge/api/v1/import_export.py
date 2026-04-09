# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from databridge.api.response import success, error


@frappe.whitelist()
def start_import(source_file=None, source_connection=None, target_doctype=None, field_mapping=None):
    """Start a data import job."""
    frappe.has_permission("DB Import Job", "create", throw=True)
    from databridge.services.import_service import ImportService
    try:
        if isinstance(field_mapping, str):
            field_mapping = frappe.parse_json(field_mapping)

        job = frappe.get_doc({
            "doctype": "DB Import Job",
            "source_file": source_file,
            "source_connection": source_connection,
            "target_doctype": target_doctype,
            "status": "Pending",
        }).insert()

        frappe.enqueue(
            "databridge.services.import_service.ImportService.process_import",
            queue="long",
            timeout=600,
            job_name=job.name,
            field_mapping=field_mapping,
        )
        return success(data={"job": job.name, "status": "Queued"}, message="Import job started")
    except Exception as e:
        frappe.log_error("DataBridge Import Error")
        return error(str(e), error_code="DB_IMPORT_FAILED")


@frappe.whitelist()
def get_import_status(job_name):
    """Get status of an import job."""
    frappe.has_permission("DB Import Job", "read", throw=True)
    job = frappe.get_doc("DB Import Job", job_name)
    return success(data={
        "name": job.name,
        "status": job.status,
        "target_doctype": job.target_doctype,
        "total_rows": job.total_rows,
        "processed_rows": job.processed_rows,
        "success_count": job.success_count,
        "error_count": job.error_count,
    })


@frappe.whitelist()
def export_data(doctype, filters=None, fields=None, file_format="CSV"):
    """Export data from a DocType."""
    frappe.has_permission(doctype, "read", throw=True)
    try:
        if isinstance(filters, str):
            filters = frappe.parse_json(filters)
        if isinstance(fields, str):
            fields = frappe.parse_json(fields)

        data = frappe.get_all(doctype,
            filters=filters or {},
            fields=fields or ["*"],
            limit_page_length=0,
        )
        return success(data={"records": data, "count": len(data), "format": file_format})
    except Exception as e:
        frappe.log_error("DataBridge Export Error")
        return error(str(e), error_code="DB_EXPORT_FAILED")
