# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "library"
app_title = "Frappe Library Management"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Library Management for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/library/css/library.bundle.css"
app_include_js = "/assets/library/js/library.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "library.engine.on_document_submit",
        "on_cancel": "library.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "library.engine.daily_scheduled_sync"
    ]
}
