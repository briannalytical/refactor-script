-- view table --
SELECT *
FROM application_tracking

-- insert new job --
INSERT INTO application_tracking (
    job_title,
    company,
    date_applied,
	application_software
)
VALUES (
    'Junior DevOps Engineer',
	'Tech Consulting',
	'2025-07-16',
	'linkedin easy apply'
	)