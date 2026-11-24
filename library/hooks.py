# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "library"
app_title = "Frappe Library Management"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Library Management - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/library/css/library.bundle.css"
app_include_js = "/assets/library/js/library.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Library Management Entry": {
        "validate": "library.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "library.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "library.tasks.hourly_sync"
    ],
    "daily": [
        "library.tasks.daily_reconciliation"
    ],
    "weekly": [
        "library.tasks.weekly_digest"
    ]
}
