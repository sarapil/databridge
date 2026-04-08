# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge — Mapping Service
Visual field mapping logic.
"""
import frappe
from frappe import _


class MappingService:
    @staticmethod
    def auto_map_fields(source_fields: list[str], target_doctype: str) -> list[dict]:
        """Auto-suggest field mappings based on name similarity."""
        target_meta = frappe.get_meta(target_doctype)
        target_fields = {f.fieldname: f.label for f in target_meta.fields if f.fieldtype not in ("Section Break", "Column Break", "Tab Break")}
        mappings = []
        for src_field in source_fields:
            src_lower = src_field.lower().replace(" ", "_").replace("-", "_")
            # Exact match
            if src_lower in target_fields:
                mappings.append({"source_field": src_field, "target_field": src_lower, "confidence": 1.0})
                continue
            # Label match
            for fname, flabel in target_fields.items():
                if flabel and src_field.lower() == flabel.lower():
                    mappings.append({"source_field": src_field, "target_field": fname, "confidence": 0.9})
                    break
        return mappings

    @staticmethod
    def validate_mapping(mapping_name: str) -> dict:
        """Validate a field map against the target DocType."""
        field_map = frappe.get_doc("DB Field Map", mapping_name)
        target_meta = frappe.get_meta(field_map.target_doctype)
        valid_fields = {f.fieldname for f in target_meta.fields}
        errors = []
        for rule in field_map.get("field_mappings", []):
            if rule.target_field not in valid_fields:
                errors.append(f"Target field '{rule.target_field}' does not exist in {field_map.target_doctype}")
        return {"valid": len(errors) == 0, "errors": errors}
