# IT Service Request Management System

## Project Overview

The IT Service Request Management System is a web-based application developed using Python and Django. It helps employees raise IT support requests and allows support staff to manage, assign, track, and resolve tickets through a centralized dashboard.

## Features

### Employee
- User login and logout.
- Create IT service requests with a title, description, category, and priority.
- View personal tickets and track their status.
- View ticket details, assigned support staff, and resolution messages.
- Add comments and communicate with support staff.

### Support Staff
- Access a dedicated support dashboard.
- View and manage all tickets.
- Assign tickets to support staff.
- Update ticket status and add resolution messages.
- Search tickets by title.
- Filter tickets by status and priority.
- View ticket statistics, including total, open, in-progress, resolved, and closed tickets.

### Validation and Access Control
- Restricts the support dashboard to staff accounts.
- Restricts ticket details to the ticket creator and support staff.
- Prevents tickets from being marked as resolved without a valid resolution message.
- Displays success and error messages after relevant actions.

## Technologies Used

- Backend: Python, Django
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite
- Tools: Visual Studio Code, Git, GitHub

## Getting Started

### Prerequisites
- Python installed on your system
- Django installed in your Python environment

### Installation

1. Clone or download this repository.
2. Open a terminal in the project folder containing `manage.py`.
3. Create and activate a virtual environment.

   ```bash
   python -m venv venv
   ```

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

4. Install Django:

   ```markdown
   Install the project dependencies:

  ```bash
pip install -r requirements.txt
   ```

5. Configure your environment variables:

   Create a `.env` file by copying `.env.example`:

   ```powershell
   Copy-Item .env.example .env
   ```

   Generate a new Django secret key:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Copy the generated key into `.env`, replacing the placeholder value for `DJANGO_SECRET_KEY`.
   Do not upload your `.env` file to GitHub.


6. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

7. Create an administrator account:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ```

9. Open `http://127.0.0.1:8000/` in your browser.

## Project Status

The project includes ticket creation, ticket tracking, role-based access checks, assignment, comments, resolution validation, search, filtering, and dashboard statistics. Further testing and improvements may be added as development continues.

<!-- # — Main project title
## — Main sections
### — Subsections within a section -->