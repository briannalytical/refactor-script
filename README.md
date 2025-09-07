# Stack Trace Job Application Tracker

A Python-based command-line tool to help you track job applications, manage follow-ups, and schedule interviews. Stay organized during your job search with automated reminders and task management!

## Features

- Track job applications with detailed status management
- Automated follow-up reminders and task scheduling
- Interview scheduling and preparation notes
- Daily task view with backlog management
- Contact information management
- Application statistics and viewing

## Prerequisites

- Python 3.7 or higher
- PostgreSQL database
- Git (optional, for cloning)

## Installation Guide

### For Windows

#### 1. Install Python
1. Download Python from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### 2. Install PostgreSQL
1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run the installer and remember your password for the `postgres` user
3. Default settings are usually fine (port 5432)
4. Add PostgreSQL to your PATH or use the full path to `psql`

#### 3. Set up the Database
1. Open Command Prompt as Administrator
2. Connect to PostgreSQL:
   ```cmd
   psql -U postgres -h localhost
   ```
3. Enter your postgres password when prompted
4. Create the database and table:
   ```sql
   CREATE DATABASE job_tracker;
   \c job_tracker;
   
   CREATE TABLE application_tracking (
       id SERIAL PRIMARY KEY,
       job_title VARCHAR(255) NOT NULL,
       company VARCHAR(255) NOT NULL,
       application_software VARCHAR(100),
       job_notes TEXT,
       follow_up_contact_name VARCHAR(255),
       follow_up_contact_details TEXT,
       application_status VARCHAR(50) DEFAULT 'applied',
       next_action VARCHAR(100),
       check_application_status DATE,
       next_follow_up_date DATE,
       interview_date DATE,
       interview_time TIME,
       interviewer_name VARCHAR(255),
       interview_prep_notes TEXT,
       second_interview_date DATE,
       final_interview_date DATE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
5. Exit PostgreSQL:
   ```sql
   \q
   ```

#### 4. Install Python Dependencies
```cmd
pip install psycopg2-binary
```

### For macOS

#### 1. Install Python
Python usually comes pre-installed, but you may want a newer version:

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

**Option B: Download from python.org**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer

Verify installation:
```bash
python3 --version
pip3 --version
```

#### 2. Install PostgreSQL

**Option A: Using Homebrew (Recommended)**
```bash
brew install postgresql
brew services start postgresql
```

**Option B: Download PostgreSQL**
1. Download from [postgresql.org](https://www.postgresql.org/download/macos/)
2. Run the installer

#### 3. Set up the Database
1. Open Terminal
2. Connect to PostgreSQL:
   ```bash
   psql postgres
   ```
3. Create the database and table:
   ```sql
   CREATE DATABASE job_tracker;
   \c job_tracker;
   
   CREATE TABLE application_tracking (
       id SERIAL PRIMARY KEY,
       job_title VARCHAR(255) NOT NULL,
       company VARCHAR(255) NOT NULL,
       application_software VARCHAR(100),
       job_notes TEXT,
       follow_up_contact_name VARCHAR(255),
       follow_up_contact_details TEXT,
       application_status VARCHAR(50) DEFAULT 'applied',
       next_action VARCHAR(100),
       check_application_status DATE,
       next_follow_up_date DATE,
       interview_date DATE,
       interview_time TIME,
       interviewer_name VARCHAR(255),
       interview_prep_notes TEXT,
       second_interview_date DATE,
       final_interview_date DATE,
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
       updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```
4. Exit PostgreSQL:
   ```sql
   \q
   ```

#### 4. Install Python Dependencies
```bash
pip3 install psycopg2-binary
```

## Configuration

### Database Connection Setup

1. Open the `job_tracker.py` file in your text editor
2. Update the database connection parameters:
   ```python
   conn = psycopg2.connect(
       dbname="job_tracker",      # Change if you used a different database name
       user="postgres",           # Change if you use a different username
       password="your_password_here",  # Replace with your actual password
       host="localhost",          # Usually localhost
       port="5432"               # Default PostgreSQL port
   )
   ```

### Security Note
For production use, consider using environment variables for sensitive information:

1. Create a `.env` file (never commit this to version control):
   ```
   DB_NAME=job_tracker
   DB_USER=postgres
   DB_PASSWORD=your_password_here
   DB_HOST=localhost
   DB_PORT=5432
   ```

2. Install python-dotenv:
   ```bash
   pip install python-dotenv
   ```

3. Update your script to use environment variables:
   ```python
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   conn = psycopg2.connect(
       dbname=os.getenv('DB_NAME'),
       user=os.getenv('DB_USER'),
       password=os.getenv('DB_PASSWORD'),
       host=os.getenv('DB_HOST'),
       port=os.getenv('DB_PORT')
   )
   ```

## Running the Application

### Windows
```cmd
python job_tracker.py
```

### macOS/Linux
```bash
python3 job_tracker.py
```

## Usage Guide

### Main Menu Options

- **VIEW**: View all applications (with option to filter active only)
- **TASKS**: View today's tasks and manage your backlog
- **ENTER**: Add a new job application
- **UPDATE**: Modify existing applications
- **TIPS**: Helpful job search tips
- **BYE**: Exit the application

### Application Statuses

The tracker supports the following status progression:
1. Applied
2. First Interview Scheduled
3. First Interview Completed
4. Post First Interview Follow-Up Sent
5. Second Interview Scheduled
6. Second Interview Completed
7. Post Second Interview Follow-Up Sent
8. Final Interview Scheduled
9. Final Interview Completed
10. Post Final Interview Follow-Up Sent
11. Offer Received
12. Rejected

### Best Practices

1. **Add applications immediately** after applying
2. **Set follow-up reminders** for 1-2 weeks after applying
3. **Update status** after each interaction
4. **Add contact information** when you find recruiters or hiring managers
5. **Check tasks daily** to stay on top of follow-ups

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'psycopg2'"**
- Solution: Run `pip install psycopg2-binary`

**"psql: command not found" (macOS)**
- Solution: Add PostgreSQL to your PATH or use the full path: `/Applications/Postgres.app/Contents/Versions/latest/bin/psql`

**Connection refused errors**
- Check if PostgreSQL service is running
- Verify host, port, username, and password in the connection string
- Make sure the database exists

**"relation 'application_tracking' does not exist"**
- Make sure you ran the CREATE TABLE command in the correct database
- Verify you're connected to the right database with `\c job_tracker`

### Getting Help

1. Check that all prerequisites are installed correctly
2. Verify your database connection parameters
3. Make sure PostgreSQL service is running
4. Try running commands step-by-step to isolate issues

## File Structure

```
job-tracker/
├── job_tracker.py          # Main application file
├── schema.sql             # Database schema file
├── README.md              # This file
├── .env                   # Environment variables (optional)
└── requirements.txt       # Python dependencies (optional)
```

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this tool!

## License

This project is open source. Use it freely for your job search success! 🚀
