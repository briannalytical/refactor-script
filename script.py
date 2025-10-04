import datetime
import psycopg2
from datetime import date

# db connection
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="your_password_here",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# fetch today's date
today = date.today()

# menu
def show_intro():
    print("\n📋 Hello! Welcome to Refactor, your job application tracker! I hope you will find this tool useful! 🥰")
    print("It's tough out there, but tracking your applications doesn't have to be!")
    print("You can use this tool to track applications, remind you when to follow up, and schedule your interviews!")
    print("You can press X + enter at any point to return to the main menu!")

def show_main_menu():
    print("\nWhat would you like to do? Enter your choice below:")
    print("\nVIEW: View all applications")
    print("TASKS: View today's tasks")
    print("ENTER: Track a new job application")
    print("UPDATE: Update an existing application")
    print("TIPS: Some helpful tips to keep in mind as you apply")
    print("BYE: End your session")
    
show_intro()

# invalid entry handling
def number_selection_invalid():
    print("\n😭 Invalid number selection. Please select from available options.")

def letter_selection_invalid():
    print("\n😭 This letter does not exist in this context. Try choosing from the available options.")

def yes_or_no_selection_invalid():
    print("\n😭 Please select Y or N.")

def yes_no_exit_selection_invalid():
    print("\nGirl just pick yes, no, or eXit. 😭")

def deletion_cancelled():
    print("\n❌ Deletion has been cancelled.")

def x_to_exit():
    print("\n🔙 Returning to main menu.")

def format_status(status):
    status_map_formatting = {
        'applied': 'Applied',
        'interviewing_first_scheduled': 'First Interview Scheduled',
        'interviewing_first_completed': 'First Interview Completed',
        'interviewing_first_followed_up': 'First Interview Completed - Follow-up Sent',
        'interviewing_second_scheduled': 'Second Interview Scheduled',
        'interviewing_second_completed': 'Second Interview Completed',
        'interviewing_second_followed_up': 'Second Interview Completed - Follow-up Sent',
        'interviewing_final_scheduled': 'Final Interview Scheduled',
        'interviewing_final_completed': 'Final Interview Completed',
        'interviewing_final_followed_up': 'Final Interview Completed - Follow-up Sent',
        'offer_received': 'Offer Received',
        'rejected': 'Rejected'
    }
    return status_map_formatting.get(status, status.replace('_', ' ').title())

while True:
    show_main_menu()
    selection = input("\nAction: ").strip().upper()

#TODO: add priority detail print text
#TODO: remove "is priority false"
    if selection == "VIEW":
        while True:
            selection = input("\nDo you want to see only active applications? (Y/N) Press X to exit: ").strip().upper()

            if selection == "Y":
                query = "SELECT company, job_title, id, application_status, date_applied, follow_up_contact_name, follow_up_contact_details FROM application_tracking WHERE application_status != 'rejected' ORDER BY company ASC, date_applied ASC"
                break
            elif selection == "N":
                query = "SELECT company, job_title, id, application_status, date_applied, follow_up_contact_name, follow_up_contact_details FROM application_tracking ORDER BY company ASC, date_applied ASC"
                break
            elif selection == "X":
                x_to_exit()
                break
            else:
                letter_selection_invalid()
                continue

        if selection != "X":
            cursor.execute(query)
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]

            if not rows:
                print("\n😶 No applications found.")
            else:
                print("\n📄 Applications")
                print("=" * 60)

                # display all applications
            for row in rows:
                company, job_title, app_id, application_status = row[0], row[1], row[2], row[3]
                print(f"{company}: {job_title} ({app_id})")
                print(f"   Status: {format_status(application_status)}")
                print("=" * 60)

            # select application id
            while True:
                selection = input("\nEnter application ID to view details, or press X to exit: ").strip().upper()
                if selection == "X":
                    x_to_exit()
                    break

                try:
                    selected_id = int(selection)
                    # find selected application
                    selected_row = None
                    for row in rows:
                        if row[2] == selected_id:
                            selected_row = row
                            break

                    # display application details
                    if selected_row:
                        print(f"\n📄 Application Details: {selected_id}")
                        print("=" * 60)

                        # display all fields for selected application
                        display_fields = [
                            (col, val) for col, val in zip(column_names, selected_row)
                            if col != "id" and val not in (None, '')
                        ]

                        if display_fields:
                            for col, val in display_fields:
                                # date and time formatting
                                if isinstance(val, datetime.date):
                                    val = val.strftime("%B %d, %Y")
                                elif isinstance(val, datetime.time):
                                    val = val.strftime("%I:%M %p")

                                # format application status specially
                                if col == "application_status":
                                    val = format_status(val)
                                if col == "follow_up_contact_name":
                                    val == format_status(val)


                                # column name formatting
                                col_clean = col.replace('_', ' ').title()
                                print(f"{col_clean}: {val}")

                            print("-" * 60)
                    else:
                        number_selection_invalid()

                except ValueError:
                    number_selection_invalid()


#TODO: display and order by priority then date applied
#TODO: automation for follow-up post interview
#TODO: prompt completion of task for backlog (function)
#TODO: show contact info details; message for if this is blank
    #TASKS: check follow-up tasks information
    elif selection == "TASKS":
        # begin backlog tasks
        backlog_query = """
            SELECT id, job_title, company, next_action,
               check_application_status, application_status, next_follow_up_date,
               interview_date, interview_time, second_interview_date, final_interview_date, is_priority
            FROM application_tracking
            WHERE (check_application_status::DATE < %s AND check_application_status IS NOT NULL)
            OR (next_follow_up_date::DATE < %s AND next_follow_up_date IS NOT NULL)
            OR (interview_date::DATE < %s AND interview_date IS NOT NULL)
            OR (second_interview_date::DATE < %s AND second_interview_date IS NOT NULL)
            OR (final_interview_date::DATE < %s AND final_interview_date IS NOT NULL)
            ORDER BY next_follow_up_date ASC;
        """
        cursor.execute(backlog_query, (today, today, today, today, today))
        backlog_rows = cursor.fetchall()

        # set default for bypassing backlog
        selection = "N"

        if backlog_rows:
            print(f"\n📋 You have {len(backlog_rows)} overdue task(s) in your backlog!")

            while True:
                selection = input("Would you like to see your backlog first? (Y/N/X): ").strip().upper()
                if selection == "X":
                    x_to_exit()
                    break
                elif selection in ['Y', 'N']:
                    break
                else:
                    yes_or_no_selection_invalid()
                    continue

            if selection == "Y":
                print(f"\n📋 Backlog - Overdue Tasks")
                print("-" * 60)
                for row in backlog_rows:
                    (app_id, job_title, company, next_action,
                     check_date, current_status, follow_up_date, interview_date,
                     interview_time, second_interview_date, final_interview_date, is_priority) = row

                    print(f"📌 {job_title} @ {company}")
                    if next_action:
                        print(f"   → Task: {next_action.replace('_', ' ').title()}")

                    overdue_dates = []
                    if check_date and check_date.date() < today:
                        overdue_dates.append(f"Check status: {check_date.strftime('%B %d, %Y')}")
                    if follow_up_date and follow_up_date.date() < today:
                        overdue_dates.append(f"Follow up: {follow_up_date.strftime('%B %d, %Y')}")
                    if interview_date and interview_date.date() < today:
                        overdue_dates.append(f"Interview: {interview_date.strftime('%B %d, %Y')}")
                    if second_interview_date and second_interview_date.date() < today:
                        overdue_dates.append(f"2nd Interview: {second_interview_date.strftime('%B %d, %Y')}")
                    if final_interview_date and final_interview_date.date() < today:
                        overdue_dates.append(f"Final Interview: {final_interview_date.strftime('%B %d, %Y')}")

                    if overdue_dates:
                        print(f"   → Overdue: {', '.join(overdue_dates)}")
                    print()
                print("-" * 60)

        # begin daily task board
        if selection == "N":
            query = """
                SELECT id, job_title, company, next_action,
                   check_application_status, application_status, next_follow_up_date,
                   interview_date, interview_time, second_interview_date, final_interview_date
                FROM application_tracking
                WHERE check_application_status::DATE = %s
                OR next_follow_up_date::DATE = %s
                OR interview_date::DATE = %s
                OR second_interview_date::DATE = %s
                OR final_interview_date::DATE = %s
                ORDER BY job_title;
            """
            cursor.execute(query, (today, today, today, today, today))
            rows = cursor.fetchall()

            if not rows:
                print("\n🎉 No tasks for today!")
            else:
                print(f"\n🗓️ Tasks for {today.strftime('%A, %B %d, %Y')}")
                print("-" * 60)

                backlog_tasks = []  # store any incomplete tasks

                for row in rows:
                    (app_id, job_title, company, next_action,
                     check_date, current_status, follow_up_date, interview_date,
                     interview_time, second_interview_date, final_interview_date) = row

                    # determine task type
                    if (interview_date == today or
                            second_interview_date == today or
                            final_interview_date == today):
                        due_type = "Interview"
                    else:
                        due_type = "Follow Up"

                    # print tasks
                    print(f"📌 {job_title} @ {company}")
                    if next_action:
                        print(f"   → Task: {next_action.replace('_', ' ').title()}")
                    print(f"   → Type: {due_type}")
                    if interview_time:
                        print(f"   → Interview Time: {interview_time.strftime('%I:%M %p')}")
                    print()

                    # task completion
                    while True:
                        selection = input("\n✅ Mark this task as completed? (Y/N): ").strip().upper()
                        if selection == "X":
                            x_to_exit()
                            break
                        elif selection in ['Y', 'N']:
                            break
                        else:
                            yes_or_no_selection_invalid()
                            continue

                    if selection == "Y":
                        auto_status_map = {
                            'check_application_status': 'interviewing_first_scheduled',
                            'follow_up_with_contact': 'interviewing_first_scheduled',
                            'send_follow_up_email': 'interviewing_first_followed_up',
                            'prepare_for_interview': 'interviewing_first_completed',
                            'send_thank_you_email': 'interviewing_first_followed_up',
                            'prepare_for_second_interview': 'interviewing_second_completed',
                            'send_thank_you_email_second_interview': 'interviewing_second_followed_up',
                            'prepare_for_final_interview': 'interviewing_final_completed',
                            'send_thank_you_email_final_interview': 'interviewing_final_followed_up'
                        }

                        if next_action and next_action in auto_status_map:
                            new_status = auto_status_map[next_action]
                            cursor.execute("""
                                UPDATE application_tracking
                                SET application_status = %s
                                WHERE id = %s;
                            """, (new_status, app_id))
                            conn.commit()
                            print(f"\n✅ Status auto-updated to: {new_status}\n")
                        else:
                            print("\n✅ Task marked as completed")

                    else:
                        backlog_tasks.append((job_title, company, next_action or "Follow up"))

#TODO: implement status method
                    # manual status update option
                    while True:
                        selection = input(
                            "\n✏️ Would you like to manually update the application status? This is for if you have jumped forward in the interview pipeline. (Y/N): ").strip().upper()
                        if selection == "X":
                            x_to_exit()
                            break
                        elif selection in ['Y', 'N']:
                            break
                        else:
                            letter_selection_invalid()
                            continue

                    if selection == "Y":
                        status_options = {
                            "Applied": "applied",
                            "First Interview Scheduled": "interviewing_first_scheduled",
                            "First Interview Completed": "interviewing_first_completed",
                            "Post First Interview Follow-Up Sent": "interviewing_first_followed_up",
                            "Second Interview Scheduled": "interviewing_second_scheduled",
                            "Second Interview Completed": "interviewing_second_completed",
                            "Post Second Interview Follow-Up Sent": "interviewing_second_followed_up",
                            "Final Interview Scheduled": "interviewing_final_scheduled",
                            "Final Interview Completed": "interviewing_final_completed",
                            "Post Final Interview Follow-Up Sent": "interviewing_final_followed_up",
                            "Offer Received": "offer_received",
                            "Rejected": "rejected"
                        }

                        print("\n📌 Please select the number that corresponds with the status you'd like to update to:")
                        labels = list(status_options.keys())

                        for i, label in enumerate(labels, 1):
                            print(f"{i}. {label}")

                        while True:
                            selection = input("Enter the number: ").strip()
                            new_status = None

                            if selection == "X":
                                x_to_exit()
                                break
                            elif selection.isdigit():
                                index = int(selection) - 1
                                if 0 <= index < len(labels):
                                    new_status = status_options[labels[index]]
                                    break
                                else:
                                    number_selection_invalid()
                                    continue
                            else:
                                lower_map = {k.lower(): v for k, v in status_options.items()}
                                if selection.lower() in lower_map:
                                    new_status = lower_map[selection.lower()]
                                    break
                                else:
                                    number_selection_invalid()
                                    continue

                        cursor.execute("""
                            UPDATE application_tracking
                            SET application_status = %s
                            WHERE id = %s;
                        """, (new_status, app_id))
                        conn.commit()
                        print(f"\n✅ Status manually updated to: {new_status}\n")
                    else:
                        print("\n⏭️ Skipped status update.\n")

                # show today's incomplete tasks
                if backlog_tasks:
                    print("\n📋 Today's Incomplete Tasks:")
                    print("-" * 60)
                    for job_title, company, task in backlog_tasks:
                        print(f"📌 {job_title} @ {company} - {task}")
                    print("-" * 60)


    # ENTER: individual application entry
    elif selection == "ENTER":
        print("\nEnter your new application details:")
        job_title = input("Job title: ").strip()
        company = input("Company: ").strip()
        software = input("How did you apply (LinkedIn, Workday, Greenhouse, company website etc): ").strip()
        notes = input("Any notes about this role? (optional): ").strip()
        while True:
            priority_input = input("Mark this job as priority? (Y/N): ").strip().upper()
            if priority_input == "Y":
                is_priority = True
                break
            elif priority_input == "N":
                is_priority = False
                break
            else:
                yes_or_no_selection_invalid()
                continue
        print("Optional now, but do your research! 🔎")
        contact_name = input("Contact Name: ").strip()
        contact_details = input("Contact Details: ").strip()

        cursor.execute("""
            INSERT INTO application_tracking (
                job_title, company, application_software, job_notes,
                follow_up_contact_name, follow_up_contact_details, is_priority
            ) VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (job_title, company, software or None, notes or None, 
          contact_name or None, contact_details or None, is_priority))

        conn.commit()
        print("\n✅ Application added! I'll remind you when you have tasks related to this job. 😊")


    # UPDATE: make updates to existing applications
#TODO: make update for priority
#TODO: handle invalid selection
    elif selection == "UPDATE":
        cursor.execute("SELECT id, job_title, company FROM application_tracking WHERE application_status != 'rejected' ORDER BY company;")
        apps = cursor.fetchall()

        if not apps:
            print("\n😶 No applications found to update.")
            continue

        print("\n--- Existing Applications ---")
        for app in apps:
            print(f"{app[0]}: {app[2]} - {app[1]}")

        while True:
            try:
                app_id = int(input("\nEnter the number of the application to update: "))
                if selection == "X":
                    x_to_exit()
                    break
                # verify the id exists
                elif any(app[0] == app_id for app in apps):
                    break
            except ValueError:
                number_selection_invalid()

        print(f"\n{app_id}: {app[2]} - {app[1]}")

#TODO: notes should append to existing notes instead of default replace
        print("\nWhat do you want to update?")
        print("1. Application status")
        print("2. Update contact info")
        print("3. Schedule interview")
        print("4. Notes")
        print("5. Delete Entry")
        
        while True:
            selection = input("\nField to update (1-5): ").strip()
            if selection == "X":
                x_to_exit()
                break
            elif selection in ['1', '2', '3', '4', '5']:
                break
            else:
                number_selection_invalid()
                continue

#TODO: show selected application when menu option comes up.
        if selection == "1":
            status_options = {
                "Applied": "applied",
                "First Interview Scheduled": "interviewing_first_scheduled",
                "First Interview Completed": "interviewing_first_completed",
                "Post First Interview Follow-Up Sent": "interviewing_first_followed_up",
                "Second Interview Scheduled": "interviewing_second_scheduled",
                "Second Interview Completed": "interviewing_second_completed",
                "Post Second Interview Follow-Up Sent": "interviewing_second_followed_up",
                "Final Interview Scheduled": "interviewing_final_scheduled",
                "Final Interview Completed": "interviewing_final_completed",
                "Post Final Interview Follow-Up Sent": "interviewing_final_followed_up",
                "Offer Received": "offer_received",
                "Rejected": "rejected"
            }

#TODO: prompt date and time entry for interviews
            print("\n📌 Select a new status:")
            labels = list(status_options.keys())
            
            for i, label in enumerate(labels, 1):
                print(f"{i}. {label}")

            while True:
                selection = input("Enter the number or status name: ").strip()
                new_status = None
                if selection == "X":
                    x_to_exit()
                    break
                elif selection.isdigit():
                    index = int(selection) - 1
                    if 0 <= index < len(labels):
                        new_status = status_options[labels[index]]
                        break
                    else:
                        number_selection_invalid()
                        continue
                else:
                    lower_map = {k.lower(): v for k, v in status_options.items()}
                    if selection.lower() in lower_map:
                        new_status = lower_map[selection.lower()]
                        break
                    else:
                        number_selection_invalid()
                        continue

            cursor.execute("""
                UPDATE application_tracking
                SET application_status = %s
                WHERE id = %s;
            """, (new_status, app_id))
            conn.commit()
            print("\n✅ Status updated.")

        elif selection == "2":
            contact_name = input("Contact name: ").strip()
            contact_details = input("Contact email/phone/URL: ").strip()
            cursor.execute("""
                UPDATE application_tracking
                SET follow_up_contact_name = %s,
                    follow_up_contact_details = %s
                WHERE id = %s;
            """, (contact_name, contact_details, app_id))
            conn.commit()
            print("\n✅ Follow-up contact updated.")

        elif selection == "3":
            interview_date = input("Enter interview date (YYYY-MM-DD): ").strip()
            interview_time = input("Enter interview time (HH:MM): ").strip()
            interview_name = input("Interviewer name: ").strip()
            prep_notes = input("Any prep notes? (optional): ").strip()

            cursor.execute("""
                UPDATE application_tracking
                SET interview_date = %s,
                    interview_time = %s,
                    interviewer_name = %s,
                    interview_prep_notes = %s
                WHERE id = %s;
            """, (interview_date, interview_time or None, interview_name, prep_notes or None, app_id))
            conn.commit()
            print("\n✅ Interview details updated.")

        elif selection == "4":
            new_notes = input("Enter your updated job notes: ").strip()
            cursor.execute("""
                UPDATE application_tracking
                SET job_notes = %s
                WHERE id = %s;
            """, (new_notes, app_id))
            conn.commit()
            print("\n✅ Notes updated.")
        
        elif selection == "5":
            cursor.execute("""
                SELECT job_title, company, application_status 
                FROM application_tracking 
                WHERE id = %s;
            """, (app_id,))
            app_details = cursor.fetchone()
            
            if app_details:
                job_title, company, status = app_details
                print(f"\n⚠️  You are about to delete:")
                print(f"   Job: {job_title}")
                print(f"   Company: {company}")
                print(f"   Status: {status}")
                
                while True:
                    selection = input("\nAre you sure you want to delete this application? (Y/N): ").strip().upper()
                    if selection == "X":
                        x_to_exit()
                        break
                    elif selection in ['Y', 'N']:
                        break
                    else:
                        yes_or_no_selection_invalid()
        
                if selection == "Y":
                    while True:
                        selection = input("This action cannot be undone. Type 'DELETE' to confirm: ").strip()
                        if selection == "DELETE":
                            break
                        elif selection.upper() == "N" or selection.upper() == "NO":
                            print("\n❌ Deletion cancelled.")
                            break
                        else:
                            print("\n❌ Please type 'DELETE' exactly to confirm, or 'N' to cancel")
            
                    if selection == "DELETE":
                        cursor.execute("DELETE FROM application_tracking WHERE id = %s;", (app_id,))
                        conn.commit()
                        print(f"\n✅ Application for {job_title} @ {company} has been deleted.")
                    else:
                        deletion_cancelled()
                else:
                    deletion_cancelled()
            else:
                print("\n❌ Application not found.")


    # TIPS: tips for job seekers
    elif selection == "TIPS":
        print("\n💡 Job Search Tips:")
        print("📩 FOLLOW UP! You are 78% more likely to land an interview if you reach out to a recruiter or hiring manager after you apply.")
        print("✏️ TAKE NOTES! You should already know why you want to work for the company and about their mission BEFORE speaking with someone from the company.")
        print("🔑 Confidence is Key! You know you deserve this job and focus on YOU, not anyone else!")
        print("💻 Keep applying, keep trying. It will not be this way forever.")

    elif selection == "BYE":
        print("\n👋 Goodbye! Check back again soon!")
        break
    
    else:
        print("\n❌ Invalid selection. 🥲 Please try again from the main menu.")

# cleanup
cursor.close()
conn.close()