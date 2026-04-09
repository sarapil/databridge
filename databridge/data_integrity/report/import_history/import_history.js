// Copyright (c) 2024, Moataz M Hassan (Arkan Lab)
// License: MIT

frappe.query_reports["Import History"] = {
	filters: [
		{
			fieldname: "status",
			label: __("Status"),
			fieldtype: "Select",
			options: "\nDraft\nIn Progress\nCompleted\nFailed\nCancelled",
		},
		{
			fieldname: "target_doctype",
			label: __("Target DocType"),
			fieldtype: "Link",
			options: "DocType",
		},
	],
};
