# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    chart = get_chart(data)
    return columns, data, None, chart


def get_columns():
    return [
        {"fieldname": "name", "label": _("Job"), "fieldtype": "Link", "options": "DB Import Job", "width": 180},
        {"fieldname": "job_name", "label": _("Job Name"), "fieldtype": "Data", "width": 200},
        {"fieldname": "target_doctype", "label": _("Target DocType"), "fieldtype": "Data", "width": 150},
        {"fieldname": "status", "label": _("Status"), "fieldtype": "Data", "width": 100},
        {"fieldname": "total_records", "label": _("Total Records"), "fieldtype": "Int", "width": 120},
        {"fieldname": "success_count", "label": _("Success"), "fieldtype": "Int", "width": 100},
        {"fieldname": "error_count", "label": _("Errors"), "fieldtype": "Int", "width": 100},
        {"fieldname": "creation", "label": _("Date"), "fieldtype": "Datetime", "width": 160},
    ]


def get_data(filters):
    conditions = {}
    if filters and filters.get("status"):
        conditions["status"] = filters["status"]
    if filters and filters.get("target_doctype"):
        conditions["target_doctype"] = filters["target_doctype"]

    return frappe.get_all(
        "DB Import Job",
        filters=conditions,
        fields=["name", "job_name", "target_doctype", "status",
                "total_records", "success_count", "error_count", "creation"],
        order_by="creation desc",
        limit=100,
    )


def get_chart(data):
    if not data:
        return None
    status_counts = {}
    for row in data:
        s = row.get("status") or "Unknown"
        status_counts[s] = status_counts.get(s, 0) + 1
    return {
        "data": {
            "labels": list(status_counts.keys()),
            "datasets": [{"name": _("Jobs"), "values": list(status_counts.values())}],
        },
        "type": "pie",
    }
