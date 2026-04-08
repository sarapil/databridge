# Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
# Developer Website: https://arkan.it.com
# License: MIT
# For license information, please see license.txt

"""
DataBridge Installation Scripts
"""
import frappe
from frappe import _


def before_install():
    """Pre-installation checks."""
    pass


def after_install():
    """Post-installation setup."""
    create_roles()
    create_settings()
    from databridge.desktop_utils import inject_app_desktop_icon
    inject_app_desktop_icon(
        app="databridge",
        label="DataBridge",
        route="/app/databridge",
        logo_url="/assets/databridge/images/databridge-logo.svg",
        bg_color="#0EA5E9",
    )
    frappe.db.commit()
    frappe.msgprint(_("DataBridge installed successfully!"))


def create_roles():
    """Create default DataBridge roles."""
    roles = [
        {"role_name": "DB Admin", "desk_access": 1, "is_custom": 1},
        {"role_name": "DB Migration Manager", "desk_access": 1, "is_custom": 1},
        {"role_name": "DB Data Operator", "desk_access": 1, "is_custom": 1},
        {"role_name": "DB Integration Manager", "desk_access": 1, "is_custom": 1},
        {"role_name": "DB Viewer", "desk_access": 1, "is_custom": 1}
    ]
    for role_data in roles:
        if not frappe.db.exists("Role", role_data["role_name"]):
            role = frappe.new_doc("Role")
            role.update(role_data)
            role.insert(ignore_permissions=True)


def create_settings():
    """Create singleton settings record if doctype exists."""
    settings_dt = "DB Settings"
    if frappe.db.exists("DocType", settings_dt):
        if not frappe.db.exists(settings_dt, settings_dt):
            settings = frappe.new_doc(settings_dt)
            settings.insert(ignore_permissions=True)


def before_uninstall():
    """Cleanup before uninstall."""
    pass
