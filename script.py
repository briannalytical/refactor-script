import psycopg2
from datetime import date

# DB connection info — customize this
conn = psycopg2.connect(
    dbname='your_db_name',
    user='your_user',
    password='your_password',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()

# Get today’s date
today = date.today()

# Query tasks for today
query = """
SELECT id, job_title, company, next_action, check_application_status, next_follow_up_date
FROM application_tracking
WHERE check_application_status = %s
   OR next_follow_up_date = %s
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