# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _
from databridge.api.response import success, error


@frappe.whitelist()
def auto_map(source_doctype, target_doctype):
    """Auto-map fields between source and target DocTypes."""
    frappe.has_permission("DB Field Map", "create", throw=True)
    from databridge.services.mapping_service import MappingService
    try:
        result = MappingService.auto_map(source_doctype, target_doctype)
        return success(data=result, message="Field mapping generated")
    except Exception as e:
        return error(str(e), error_code="DB_MAPPING_FAILED")


@frappe.whitelist()
def get_fields(doctype):
    """Get field list for a DocType (for mapping UI)."""
    frappe.has_permission(doctype, "read", throw=True)
    meta = frappe.get_meta(doctype)
    fields = [{
        "fieldname": f.fieldname,
        "fieldtype": f.fieldtype,
        "label": f.label,
        "reqd": f.reqd,
        "options": f.options,
    } for f in meta.fields if f.fieldtype not in ("Section Break", "Column Break", "Tab Break")]
    return success(data=fields)


@frappe.whitelist()
def validate_data(doctype, data):
    """Validate data against a DocType's schema."""
    frappe.has_permission(doctype, "read", throw=True)
    from databridge.services.validation_service import ValidationService
    try:
        if isinstance(data, str):
            data = frappe.parse_json(data)
        result = ValidationService.validate_batch(doctype, data)
        return success(data=result)
    except Exception as e:
        return error(str(e), error_code="DB_VALIDATION_FAILED")
