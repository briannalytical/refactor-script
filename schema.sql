-- create table enum --
CREATE TYPE application_status_enum AS ENUM (
    'applied',
    'interviewing_first_scheduled',
    'interviewing_first_completed',
    'interviewing_first_followed_up',
    'interviewing_second_scheduled',
    'interviewing_second_completed',
    'interviewing_second_followed_up',
    'interviewing_final_scheduled',
    'interviewing_final_completed',
    'interviewing_final_followed_up',
    'offer_received',
    'rejected'
);

-- create table --
CREATE TABLE application_tracking (
    id SERIAL PRIMARY KEY,
    job_title TEXT NOT NULL,
    company TEXT NOT NULL,
    application_software TEXT,
    date_applied TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_status application_status_enum DEFAULT 'applied',
    job_notes TEXT,
    next_action TEXT,
    check_application_status TIMESTAMP,
    follow_up_contact_name TEXT,
    follow_up_contact_details TEXT,
    -- First interview
    interviewer_name TEXT,
    interviewer_contact_details TEXT,
    interview_date TIMESTAMP,
    interview_prep_notes TEXT,
    interview_post_notes TEXT,
    -- Second interview
    second_interviewer_name TEXT,
    second_interviewer_contact_details TEXT,
    second_interview_date TIMESTAMP,
    second_interview_prep_notes TEXT,
    second_interview_post_notes TEXT,
    -- Final interview
    final_interviewer_name TEXT,
    final_interviewer_contact_details TEXT,
    final_interview_date TIMESTAMP,
    final_interview_prep_notes TEXT,
    final_interview_post_notes TEXT,
    -- Offer details
    offer_details TEXT
)