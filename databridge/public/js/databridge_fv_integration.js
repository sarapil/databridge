// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT

// DataBridge — frappe_visual Integration
frappe.provide("databridge.visual");

databridge.visual.init = function () {
    if (!frappe.visual) return;
    if (frappe.visual.themeManager) {
        frappe.visual.themeManager.registerApp("databridge", {
            label: __("DataBridge"),
            color: "#0EA5E9",
            icon: "database",
        });
    }
};

if (frappe.visual) {
    databridge.visual.init();
} else {
    $(document).on("frappe_visual_ready", databridge.visual.init);
}
