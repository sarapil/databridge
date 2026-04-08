// Copyright (c) 2024, Arkan Lab — https://arkan.it.com
// License: MIT
// frappe_visual Integration for DataBridge

(function() {
    "use strict";

    const APP_CONFIG = {
        name: "databridge",
        title: __("DataBridge"),
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
