# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

"""
DataBridge — Seed Data
Runs on `after_migrate` to ensure reference data exists.
"""
import frappe
from frappe import _


def seed_data():
    """Idempotent seed — safe to run multiple times."""
    _seed_settings()
    _seed_validation_rules()
    frappe.db.commit()


def _seed_settings():
    settings_dt = "DB Settings"
    if not frappe.db.exists("DocType", settings_dt):
        return
    try:
        if not frappe.db.exists(settings_dt, settings_dt):
            frappe.new_doc(settings_dt).insert(ignore_permissions=True)
    except Exception:
        pass


def _seed_validation_rules():
    if not frappe.db.exists("DocType", "DB Validation Rule"):
        return
    rules = [
        {
            "rule_name": "Email Format",
            "rule_type": "Regex",
            "format_regex": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            "error_message": _("Invalid email address format"),
            "enabled": 1,
        },
        {
            "rule_name": "Phone International",
            "rule_type": "Regex",
            "format_regex": r"^\+?[1-9]\d{6,14}$",
            "error_message": _("Invalid international phone number"),
            "enabled": 1,
        },
        {
            "rule_name": "URL Format",
            "rule_type": "Regex",
            "format_regex": r"^https?://[^\s/$.?#].[^\s]*$",
            "error_message": _("Invalid URL format"),
            "enabled": 1,
        },
        {
            "rule_name": "Positive Number",
            "rule_type": "Range",
            "min_value": 0,
            "error_message": _("Value must be a positive number"),
            "enabled": 1,
        },
        {
            "rule_name": "Percentage",
            "rule_type": "Range",
            "min_value": 0,
            "max_value": 100,
            "error_message": _("Value must be between 0 and 100"),
            "enabled": 1,
        },
        {
            "rule_name": "Non-Empty",
            "rule_type": "Required",
            "error_message": _("This field is required"),
            "enabled": 1,
        },
    ]
    for rule in rules:
        if not frappe.db.exists("DB Validation Rule", {"rule_name": rule["rule_name"]}):
            try:
                doc = frappe.new_doc("DB Validation Rule")
                doc.update(rule)
                doc.insert(ignore_permissions=True)
            except frappe.MandatoryError:
                # Generic template rules lack target_doctype/field_name — skip
                pass
