import psycopg2
from datetime import date

# Connect to the database
conn = psycopg2.connect(
    dbname="breembair",  # or "postgres" if that's where your table lives
    user="postgres",
    password="your_password_here",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Get today’s date
today = date.today()

# ---------- MAIN MENU ----------
print("\n📋 What would you like to do?")
print("1. View today’s tasks")
print("2. Add a new job application")
print("3. Update an existing application")

choice = input("Enter 1, 2, or 3: ").strip()

# ---------- OPTION 1: Today's Tasks ----------
if choice == "1":
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
        print("\n🎉 No tasks for today!")
    else:
        print(f"\n🗓️ Tasks for {today.strftime('%A, %B %d, %Y')}")
        print("-" * 50)
        for row in rows:
            app_id, job_title, company, next_action, check_date, follow_up_date = row
            due_type = "Check status" if check_date == today else "Follow up"
            print(f"📌 {job_title} @ {company}")
            print(f"   → Task: {next_action.replace('_', ' ').title()}")
            print(f"   → Type: {due_type}")
            print()

# ---------- OPTION 2: Add a New Application ----------
elif choice == "2":
    print("\n--- New Job Application ---")
    job_title = input("Job title: ").strip()
    company = input("Company: ").strip()
    software = input("Application software (LinkedIn, Greenhouse, etc): ").strip()
    notes = input("Any job notes? (optional): ").strip()

    cursor.execute("""
        INSERT INTO application_tracking (job_title, company, application_software, job_notes)
        VALUES (%s, %s, %s, %s);
    """, (job_title, company, software or None, notes or None))

    conn.commit()
    print("✅ Application added!")

# ---------- OPTION 3: Update Existing ----------
elif choice == "3":
    cursor.execute("SELECT id, job_title, company FROM application_tracking ORDER BY id;")
    apps = cursor.fetchall()

    print("\n--- Existing Applications ---")
    for app in apps:
        print(f"{app[0]}: {app[1]} @ {app[2]}")

    app_id = int(input("\nEnter the ID of the application you want to update: "))
    print("\nWhat do you want to update?")
    print("→ status, interview, followup, or notes")
    field = input("Field to update: ").strip().lower()

    if field == "status":
        print("\nAvailable status values:")
        print("→ applied, interviewing_first_scheduled, interviewing_first_completed, etc.")
        new_status = input("New application status: ").strip()
        cursor.execute("""
            UPDATE application_tracking
            SET application_status = %s
            WHERE id = %s;
        """, (new_status, app_id))

    elif field == "interview":
        interview_date = input("Enter interview date (YYYY-MM-DD): ").strip()
        interview_name = input("Interviewer name: ").strip()
        prep_notes = input("Any prep notes? (optional): ").strip()

        cursor.execute("""
            UPDATE application_tracking
            SET interview_date = %s,
                interviewer_name = %s,
                interview_prep_notes = %s
            WHERE id = %s;
        """, (interview_date, interview_name, prep_notes or None, app_id))

    elif field == "followup":
        contact_name = input("Contact name: ").strip()
        contact_details = input("Contact email/phone: ").strip()
        cursor.execute("""
            UPDATE application_tracking
            SET follow_up_contact_name = %s,
                follow_up_contact_details = %s
            WHERE id = %s;
        """, (contact_name, contact_details, app_id))

    elif field == "notes":
        new_notes = input("Enter your updated job notes: ").strip()
        cursor.execute("""
            UPDATE application_tracking
            SET job_notes = %s
            WHERE id = %s;
        """, (new_notes, app_id))

    conn.commit()
    print("✅ Application updated.")

else:
    print("❌ Invalid selection.")

# ---------- CLEANUP ----------
cursor.close()
conn.close()