# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# License: MIT

import frappe
import pytest


@pytest.fixture
def db_source_connection():
    """Create a test DB Source Connection."""
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DB Source Connection",
        "connection_name": f"Test Conn {name}",
        "source_type": "API",
        "enabled": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    yield doc
    if frappe.db.exists("DB Source Connection", doc.name):
        frappe.delete_doc("DB Source Connection", doc.name, force=True)
        frappe.db.commit()


@pytest.fixture
def db_field_map():
    """Create a test DB Field Map."""
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DB Field Map",
        "map_name": f"Test Map {name}",
        "target_doctype": "Customer",
        "enabled": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    yield doc
    if frappe.db.exists("DB Field Map", doc.name):
        frappe.delete_doc("DB Field Map", doc.name, force=True)
        frappe.db.commit()


@pytest.fixture
def db_import_job():
    """Create a test DB Import Job."""
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DB Import Job",
        "job_name": f"Test Import {name}",
        "target_doctype": "Customer",
        "status": "Draft",
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    yield doc
    if frappe.db.exists("DB Import Job", doc.name):
        frappe.delete_doc("DB Import Job", doc.name, force=True)
        frappe.db.commit()


@pytest.fixture
def db_validation_rule():
    """Create a test DB Validation Rule."""
    name = frappe.generate_hash(length=10)
    doc = frappe.get_doc({
        "doctype": "DB Validation Rule",
        "rule_name": f"Test Rule {name}",
        "target_doctype": "Customer",
        "field_name": "customer_name",
        "validation_type": "Required",
        "enabled": 1,
    })
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    yield doc
    if frappe.db.exists("DB Validation Rule", doc.name):
        frappe.delete_doc("DB Validation Rule", doc.name, force=True)
        frappe.db.commit()
