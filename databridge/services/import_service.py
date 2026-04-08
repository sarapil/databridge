# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge — Import Service
Enhanced CSV/Excel/JSON import with validation.
"""
import frappe
from frappe import _


class ImportService:
    @staticmethod
    def create_import_job(source_file: str, target_doctype: str, mapping_name: str | None = None) -> str:
        """Create a new import job."""
        frappe.has_permission("DB Import Job", "create", throw=True)
        job = frappe.new_doc("DB Import Job")
        job.source_file = source_file
        job.target_doctype = target_doctype
        job.mapping = mapping_name
        job.status = "Pending"
        job.insert()
        return job.name

    @staticmethod
    def execute_import(job_name: str):
        """Execute an import job (background)."""
        job = frappe.get_doc("DB Import Job", job_name)
        if job.status not in ("Pending", "Retry"):
            return
        job.db_set("status", "Processing")
        frappe.db.commit()

        try:
            file_doc = frappe.get_doc("File", {"file_url": job.source_file})
            file_path = file_doc.get_full_path()

            if file_path.endswith(".csv"):
                data = ImportService._parse_csv(file_path)
            elif file_path.endswith((".xlsx", ".xls")):
                data = ImportService._parse_excel(file_path)
            else:
                frappe.throw(_("Unsupported file format"))

            success_count = 0
            error_count = 0

            for idx, row in enumerate(data, start=1):
                try:
                    mapped = ImportService._apply_mapping(row, job.mapping, job.target_doctype)
                    doc = frappe.new_doc(job.target_doctype)
                    doc.update(mapped)
                    doc.insert(ignore_permissions=True)
                    success_count += 1
                except Exception as e:
                    error_count += 1
                    _log_import_error(job.name, idx, str(e), row)

            job.db_set("status", "Completed" if error_count == 0 else "Completed with Errors")
            job.db_set("records_processed", success_count + error_count)
            job.db_set("records_success", success_count)
            job.db_set("records_failed", error_count)
        except Exception as e:
            job.db_set("status", "Failed")
            job.db_set("error_message", str(e)[:500])
            frappe.log_error(title=f"Import job failed: {job_name}")
        frappe.db.commit()

    @staticmethod
    def _parse_csv(file_path: str) -> list[dict]:
        import csv
        import chardet
        with open(file_path, "rb") as f:
            raw = f.read()
        encoding = chardet.detect(raw)["encoding"] or "utf-8"
        lines = raw.decode(encoding).splitlines()
        reader = csv.DictReader(lines)
        return list(reader)

    @staticmethod
    def _parse_excel(file_path: str) -> list[dict]:
        import openpyxl
        wb = openpyxl.load_workbook(file_path, read_only=True)
        ws = wb.active
        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            return []
        headers = [str(h or "").strip() for h in rows[0]]
        return [dict(zip(headers, row)) for row in rows[1:]]

    @staticmethod
    def _apply_mapping(row: dict, mapping_name: str | None, target_doctype: str) -> dict:
        if not mapping_name:
            return row
        field_map = frappe.get_doc("DB Field Map", mapping_name)
        mapped = {}
        for rule in field_map.get("field_mappings", []):
            source_val = row.get(rule.source_field, "")
            if rule.transform:
                source_val = _apply_transform(source_val, rule.transform)
            if source_val or rule.default_value:
                mapped[rule.target_field] = source_val or rule.default_value
        return mapped


def _log_import_error(job_name, row_number, error_message, data):
    if frappe.db.exists("DocType", "DB Import Log"):
        frappe.get_doc({
            "doctype": "DB Import Log",
            "job": job_name,
            "row_number": row_number,
            "status": "Error",
            "error_message": error_message[:500],
        }).insert(ignore_permissions=True)


def _apply_transform(value, transform_name):
    transforms = {
        "title_case": lambda v: str(v).title(),
        "trim_whitespace": lambda v: str(v).strip(),
        "lowercase": lambda v: str(v).lower(),
        "uppercase": lambda v: str(v).upper(),
    }
    fn = transforms.get(transform_name)
    return fn(value) if fn else value
