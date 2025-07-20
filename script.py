import psycopg2
from datetime import date

# db connection info
conn = psycopg2.connect(
    dbname='stack_trace_application_tracker',
    user='postgres',
    password='Mozto@35573getit',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()

# get today’s date
today = date.today()

# pull actions/tasks
query = """
SELECT id, job_title, company, next_action, check_application_status, next_follow_up_date
FROM application_tracking
WHERE check_application_status::date = %s
   OR next_follow_up_date::date = %s
ORDER BY job_title;
"""

cursor.execute(query, (today, today))
rows = cursor.fetchall()

if not rows:
    print("🎉 No tasks for today!")
else:
    print(f"🗓️ Tasks for {today.strftime('%A, %B %d, %Y')}")
    print("-" * 50)
    for row in rows:
        app_id, job_title, company, next_action, check_date, follow_up_date = row
        due_type = "Check status" if check_date == today else "Follow up"
        print(f"📌 {job_title} @ {company}")
        print(f"   → Task: {next_action.replace('_', ' ').title()}")
        print(f"   → Type: {due_type}")
        print()

cursor.close()
conn.close()