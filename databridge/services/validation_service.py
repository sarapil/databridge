# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge — Data Validation Service
"""
import frappe
from frappe import _


class ValidationService:
    @staticmethod
    def validate_data(data: list[dict], target_doctype: str) -> list[dict]:
        """Validate data rows against doctype schema and custom validation rules."""
        meta = frappe.get_meta(target_doctype)
        required_fields = [f.fieldname for f in meta.fields if f.reqd]
        errors = []
        for idx, row in enumerate(data, 1):
            for field in required_fields:
                if not row.get(field):
                    errors.append({"row": idx, "field": field, "error": _("Required field missing")})
        return errors

    @staticmethod
    def detect_duplicates(data: list[dict], target_doctype: str, match_fields: list[str]) -> list[dict]:
        """Find potential duplicate records."""
        duplicates = []
        seen = {}
        for idx, row in enumerate(data, 1):
            key = tuple(str(row.get(f, "")).strip().lower() for f in match_fields)
            if key in seen:
                duplicates.append({"row": idx, "duplicate_of_row": seen[key]})
            else:
                seen[key] = idx
        return duplicates
