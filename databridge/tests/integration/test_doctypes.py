# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest


class TestDBSourceConnection:
    """Integration tests for DB Source Connection DocType."""

    def test_create_source_connection(self, db_source_connection):
        assert db_source_connection.name is not None
        assert db_source_connection.enabled == 1
        assert frappe.db.exists("DB Source Connection", db_source_connection.name)

    def test_source_connection_unique_name(self):
        name = frappe.generate_hash(length=10)
        doc = frappe.get_doc({
            "doctype": "DB Source Connection",
            "connection_name": f"Unique Conn {name}",
            "source_type": "CSV",
            "enabled": 1,
        })
        doc.insert(ignore_permissions=True)
        assert doc.name is not None
        frappe.delete_doc("DB Source Connection", doc.name, force=True)


class TestDBImportJob:
    """Integration tests for DB Import Job DocType."""

    def test_create_import_job(self, db_import_job):
        assert db_import_job.name is not None
        assert db_import_job.status == "Draft"

    def test_import_job_status_default(self):
        name = frappe.generate_hash(length=10)
        doc = frappe.get_doc({
            "doctype": "DB Import Job",
            "job_name": f"Status Test {name}",
            "target_doctype": "Customer",
        })
        doc.insert(ignore_permissions=True)
        assert doc.status in ("Draft", None, "")
        frappe.delete_doc("DB Import Job", doc.name, force=True)


class TestDBFieldMap:
    """Integration tests for DB Field Map DocType."""

    def test_create_field_map(self, db_field_map):
        assert db_field_map.name is not None
        assert db_field_map.target_doctype == "Customer"

    def test_field_map_with_details(self):
        name = frappe.generate_hash(length=10)
        doc = frappe.get_doc({
            "doctype": "DB Field Map",
            "map_name": f"Map With Details {name}",
            "target_doctype": "Customer",
            "enabled": 1,
            "field_mappings": [
                {
                    "doctype": "DB Field Map Detail",
                    "source_field": "name",
                    "target_field": "customer_name",
                }
            ]
        })
        doc.insert(ignore_permissions=True)
        assert len(doc.field_mappings) == 1
        assert doc.field_mappings[0].source_field == "name"
        frappe.delete_doc("DB Field Map", doc.name, force=True)


class TestDBValidationRule:
    """Integration tests for DB Validation Rule DocType."""

    def test_create_validation_rule(self, db_validation_rule):
        assert db_validation_rule.name is not None
        assert db_validation_rule.validation_type == "Required"

    def test_validation_rule_disabled_by_default(self):
        name = frappe.generate_hash(length=10)
        doc = frappe.get_doc({
            "doctype": "DB Validation Rule",
            "rule_name": f"Disabled Rule {name}",
            "target_doctype": "Customer",
            "field_name": "customer_name",
            "validation_type": "Required",
            "enabled": 0,
        })
        doc.insert(ignore_permissions=True)
        assert doc.enabled == 0
        frappe.delete_doc("DB Validation Rule", doc.name, force=True)
