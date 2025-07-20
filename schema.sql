-- enum type for application status
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

-- enum type for follow-up actions
CREATE TYPE follow_up_action_enum AS ENUM (
    'check_application_status',
    'send_follow_up_email',
    'prepare_for_interview',
    'send_thank_you_email'
);

-- table definition
CREATE TABLE application_tracking (
    id SERIAL PRIMARY KEY,
    job_title TEXT NOT NULL,
    company TEXT NOT NULL,
    application_software TEXT,
    date_applied TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    application_status application_status_enum DEFAULT 'applied',
    job_notes TEXT,
    next_action follow_up_action_enum DEFAULT 'check_application_status',
    check_application_status TIMESTAMP,
    next_follow_up_date TIMESTAMP,
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
);

-- logic to exclude weekends
CREATE OR REPLACE FUNCTION add_weekdays(start_date DATE, num_days INT)
RETURNS DATE AS $$
DECLARE
    curr_date DATE := start_date;
    added_days INT := 0;
BEGIN
    WHILE added_days < num_days LOOP
        curr_date := curr_date + 1;
        IF EXTRACT(DOW FROM curr_date) NOT IN (0, 6) THEN
            added_days := added_days + 1;
        END IF;
    END LOOP;
    RETURN curr_date;
END;
$$ LANGUAGE plpgsql;

-- trigger function to auto-fill follow-up dates
CREATE OR REPLACE FUNCTION set_follow_up_dates()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.check_application_status IS NULL THEN
        NEW.check_application_status := add_weekdays(NEW.date_applied::DATE, 2);
    END IF;

    IF NEW.next_follow_up_date IS NULL THEN
        NEW.next_follow_up_date := add_weekdays(NEW.check_application_status::DATE, 1);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- trigger function that runs before insert
CREATE TRIGGER populate_follow_up_dates
BEFORE INSERT ON application_tracking
FOR EACH ROW
EXECUTE FUNCTION set_follow_up_dates();