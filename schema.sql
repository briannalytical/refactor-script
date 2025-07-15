CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    job_title TEXT NOT NULL,
    company TEXT NOT NULL,
    date_applied DATE,
    application_status TEXT DEFAULT 'applied',
	next_action TEXT DEFAULT 'check application status',
    check_application_status DATE,
    application_software TEXT NOT NULL
);