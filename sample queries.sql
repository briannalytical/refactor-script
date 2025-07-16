INSERT INTO job_applications (job_title, company, application_software)
VALUES ('Junior DevOps Engineer', 'Tech Consulting', 'LinkedIn Easy Apply');

SELECT *
FROM job_applications

ALTER TABLE job_applications
ALTER COLUMN date_applied TYPE TIMESTAMP
USING date_applied::timestamp,
ALTER COLUMN date_applied SET DEFAULT NOW();

ALTER TABLE job_applications
ADD COLUMN notes TEXT;

UPDATE job_applications
SET date_applied = '2024-07-12'
WHERE id = 1