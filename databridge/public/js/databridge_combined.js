/* databridge — Combined JS (reduces HTTP requests) */
/* Auto-generated from 2 individual files */


/* === databridge_boot.js === */
// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// Developer Website: https://arkan.it.com
// License: MIT

// DataBridge — Global Bootstrap
(function() {
"use strict";
// Guard: skip if frappe core not loaded (transient HTTP/2 proxy failures)
if (typeof frappe === "undefined" || typeof frappe.provide !== "function") return;
frappe.provide("databridge");

databridge.COLORS = {
    primary: "#0EA5E9",
    secondary: "#7DD3FC",
    success: "#10B981",
    warning: "#F59E0B",
    danger: "#EF4444",
};

// Real-time progress updates for import/sync jobs
frappe.realtime.on("db_import_progress", (data) => {
    if (data && data.job_name) {
        frappe.show_alert({
            message: __("Import {0}: {1}% complete", [data.job_name, data.progress || 0]),
            indicator: data.progress >= 100 ? "green" : "blue",
        });
    }
});

frappe.realtime.on("db_sync_status", (data) => {
    if (data && data.sync_name) {
        frappe.show_alert({
            message: __("Sync {0}: {1}", [data.sync_name, data.status]),
            indicator: data.status === "Success" ? "green" : "orange",
        });
    }
});
})();


/* === fv_integration.js === */
// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for DataBridge

(function() {
    "use strict";

    const APP_CONFIG = {
        name: "databridge",
        title: "DataBridge",
        color: "#0EA5E9",
        module: "DataBridge",
    };

    $(document).on("app_ready", function() {
        if (frappe.visual && frappe.visual.ThemeManager) {
            try {
                frappe.visual.ThemeManager.registerApp(APP_CONFIG);
            } catch(e) {
                // frappe_visual not yet loaded
            }
        }
    });
})();

