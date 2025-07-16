CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    job_title TEXT NOT NULL,
    company TEXT NOT NULL,
    date_applied TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_software TEXT NOT NULL,
    application_status TEXT DEFAULT 'applied',
    next_action TEXT DEFAULT 'check application status',
    check_application_status TIMESTAMP,
    checked_application BOOLEAN NOT NULL,
    follow_up_contact_name TEXT,
    follow_up_contact_details TEXT,
    notes TEXT
);