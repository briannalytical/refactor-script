Setup Guide

This guide will help you set up the local development environment for this Python project with PostgreSQL database.

Prerequisites
Python 3.8 or higher
Git (for cloning the repository)

Setup Instructions

macOS Setup
1. Install PostgreSQL
Option A: Using Homebrew (Recommended)
bash# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Add PostgreSQL to PATH (add to your ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
Option B: Using PostgreSQL Installer

Download from postgresql.org
Run the installer and follow the setup wizard
Remember the password you set for the postgres user

2. Create Database and User
bash# Connect to PostgreSQL
psql postgres

# Create a new database
CREATE DATABASE your_project_db;

# Create a new user (optional, you can use postgres user)
CREATE USER your_username WITH PASSWORD 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE your_project_db TO your_username;

# Exit PostgreSQL
\q
3. Set up Python Environment
bash# Clone the repository
git clone <your-repo-url>
cd <your-project-directory>

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
4. Configure Environment Variables
bash# Create a .env file in the project root
touch .env

# Add the following to .env file
echo "DB_HOST=localhost" >> .env
echo "DB_PORT=5432" >> .env
echo "DB_NAME=your_project_db" >> .env
echo "DB_USER=your_username" >> .env
echo "DB_PASSWORD=your_password" >> .env
Windows Setup
1. Install PostgreSQL

Download PostgreSQL installer from postgresql.org
Run the installer as administrator
Follow the installation wizard:

Choose installation directory (default is fine)
Select components (ensure PostgreSQL Server and pgAdmin are selected)
Set data directory (default is fine)
Set password for the postgres superuser (remember this!)
Set port (default 5432 is fine)
Choose locale (default is fine)


Complete the installation

2. Add PostgreSQL to PATH

Open System Properties (Right-click "This PC" → Properties → Advanced system settings)
Click "Environment Variables"
Under "System Variables", find and select "Path", then click "Edit"
Click "New" and add: C:\Program Files\PostgreSQL\15\bin (adjust version number if different)
Click "OK" to close all dialogs

3. Create Database and User
cmd# Open Command Prompt or PowerShell as administrator
# Connect to PostgreSQL (you'll be prompted for the postgres password)
psql -U postgres -h localhost

# Create a new database
CREATE DATABASE your_project_db;

# Create a new user (optional, you can use postgres user)
CREATE USER your_username WITH PASSWORD 'your_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE your_project_db TO your_username;

# Exit PostgreSQL
\q
4. Set up Python Environment
cmd# Clone the repository
git clone <your-repo-url>
cd <your-project-directory>

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
5. Configure Environment Variables
cmd# Create a .env file in the project root
echo. > .env

# Add environment variables to .env file (edit with notepad or your preferred editor)
notepad .env
Add the following content to the .env file:
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_project_db
DB_USER=your_username
DB_PASSWORD=your_password
Running the Project
Start the Application
bash# Make sure your virtual environment is activated
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# Run the main script
python main.py
Verify Database Connection
bash# Test database connection
python -c "
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        port=os.getenv('DB_PORT'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    print('✅ Database connection successful!')
    conn.close()
except Exception as e:
    print(f'❌ Database connection failed: {e}')
"
Common Issues and Solutions
PostgreSQL Issues
Issue: "psql: command not found"

macOS: Ensure PostgreSQL is in your PATH or use full path: /opt/homebrew/bin/psql
Windows: Add PostgreSQL bin directory to your system PATH

Issue: "password authentication failed"

Double-check your username and password
Ensure the user has proper permissions on the database

Issue: "could not connect to server"

Ensure PostgreSQL service is running:

macOS: brew services start postgresql@15
Windows: Check Services app for PostgreSQL service



Python Issues
Issue: "No module named 'psycopg2'"
bash# Install the PostgreSQL adapter
pip install psycopg2-binary
Issue: Virtual environment not activating

Ensure you're in the correct project directory
Try creating a new virtual environment if the current one is corrupted

Dependencies
Make sure your requirements.txt includes:
psycopg2-binary>=2.9.0
python-dotenv>=0.19.0
Environment Variables
VariableDescriptionExampleDB_HOSTDatabase hostlocalhostDB_PORTDatabase port5432DB_NAMEDatabase nameyour_project_dbDB_USERDatabase usernameyour_usernameDB_PASSWORDDatabase passwordyour_password
Next Steps

Customize the database schema according to your project needs
Update the connection parameters in your Python script
Run any necessary database migrations
Start developing your application!

Support
If you encounter any issues during setup, please:

Check the PostgreSQL logs for database-related issues
Verify all environment variables are correctly set
Ensure your virtual environment is activated when running Python commands
