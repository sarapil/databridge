# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge — Pre-built Import Templates for Arkan Lab Apps

Provides ready-to-use column mapping definitions for common migration
scenarios so users don't have to manually map columns:

- ARKSpace:  Tenant/member spreadsheet → AS Member
- ClinicFlow: Patient data from legacy CSV → CF Patient
- Vertex:    Contractor list → VX Subcontractor
- Candela:   Menu items → CD Menu Item
"""
import frappe
from frappe import _


# Each template: source column names → target fieldnames
IMPORT_TEMPLATES: dict[str, dict] = {
    "arkspace_members": {
        "label": "ARKSpace — Members / Tenants",
        "label_ar": "أركسبيس — الأعضاء / المستأجرين",
        "target_doctype": "AS Member",
        "field_mappings": [
            {"source_field": "Full Name", "target_field": "member_name"},
            {"source_field": "Email", "target_field": "email"},
            {"source_field": "Phone", "target_field": "phone"},
            {"source_field": "Company", "target_field": "company_name"},
            {"source_field": "Membership Type", "target_field": "membership_type"},
            {"source_field": "Start Date", "target_field": "start_date"},
            {"source_field": "End Date", "target_field": "end_date"},
            {"source_field": "Status", "target_field": "status"},
            {"source_field": "ID Number", "target_field": "id_number"},
            {"source_field": "Notes", "target_field": "notes"},
        ],
    },
    "clinicflow_patients": {
        "label": "ClinicFlow — Patient Migration",
        "label_ar": "كلينك فلو — نقل بيانات المرضى",
        "target_doctype": "CF Patient",
        "field_mappings": [
            {"source_field": "Patient Name", "target_field": "patient_name"},
            {"source_field": "Date of Birth", "target_field": "date_of_birth"},
            {"source_field": "Gender", "target_field": "gender"},
            {"source_field": "Phone", "target_field": "phone"},
            {"source_field": "Email", "target_field": "email"},
            {"source_field": "Blood Type", "target_field": "blood_group"},
            {"source_field": "National ID", "target_field": "national_id"},
            {"source_field": "Insurance Provider", "target_field": "insurance_provider"},
            {"source_field": "Insurance Number", "target_field": "insurance_number"},
            {"source_field": "Allergies", "target_field": "allergies"},
            {"source_field": "Emergency Contact", "target_field": "emergency_contact"},
            {"source_field": "Emergency Phone", "target_field": "emergency_phone"},
        ],
    },
    "vertex_subcontractors": {
        "label": "Vertex — Subcontractor Import",
        "label_ar": "فيرتكس — استيراد المقاولين الفرعيين",
        "target_doctype": "VX Subcontractor",
        "field_mappings": [
            {"source_field": "Company Name", "target_field": "company_name"},
            {"source_field": "Contact Person", "target_field": "contact_person"},
            {"source_field": "Phone", "target_field": "phone"},
            {"source_field": "Email", "target_field": "email"},
            {"source_field": "Trade", "target_field": "trade"},
            {"source_field": "License Number", "target_field": "license_number"},
            {"source_field": "Rating", "target_field": "rating"},
        ],
    },
    "candela_menu": {
        "label": "Candela — Menu Item Import",
        "label_ar": "كانديلا — استيراد قائمة الطعام",
        "target_doctype": "CD Menu Item",
        "field_mappings": [
            {"source_field": "Item Name", "target_field": "item_name"},
            {"source_field": "Name AR", "target_field": "item_name_ar"},
            {"source_field": "Category", "target_field": "category"},
            {"source_field": "Price", "target_field": "price"},
            {"source_field": "Description", "target_field": "description"},
            {"source_field": "Calories", "target_field": "calories"},
            {"source_field": "Available", "target_field": "is_available"},
        ],
    },
}


def seed_import_templates():
    """Seed pre-built DB Field Map records for each template.

    Called from databridge.seed.seed_data() — idempotent.
    """
    for key, tpl in IMPORT_TEMPLATES.items():
        template_name = f"DB-TPL-{key.upper()}"
        if frappe.db.exists("DB Field Map", template_name):
            continue
        if not frappe.db.exists("DocType", tpl["target_doctype"]):
            continue
        try:
            doc = frappe.new_doc("DB Field Map")
            doc.name1 = template_name
            doc.label = tpl["label"]
            doc.target_doctype = tpl["target_doctype"]
            doc.is_template = 1
            for mapping in tpl["field_mappings"]:
                doc.append("field_mappings", {
                    "source_field": mapping["source_field"],
                    "target_field": mapping["target_field"],
                })
            doc.insert(ignore_permissions=True)
        except Exception:
            frappe.log_error(
                title=f"DataBridge: failed to seed template {template_name}",
            )
