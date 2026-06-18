# Campus IT Helpdesk Portal

A practical Django project for managing IT support tickets, campus devices, technician assignments, troubleshooting notes, and support reports.

This project is designed as a realistic junior IT / helpdesk portfolio project. It is not just a CRUD demo. It shows how an IT support team could document user problems, assign technicians, track device-related issues, and export a support report.

## What this project demonstrates

- IT support workflow understanding
- Django web development
- SQLite database design
- User authentication
- Role-based helpdesk logic
- Asset/device tracking
- Ticket status and priority management
- Troubleshooting documentation
- CSV reporting
- Testing basics
- Clean project structure
- GitHub-ready documentation

## Main features

### Ticket Management

- Create support tickets
- Assign tickets to technicians
- Track priority, status, category, impact, and urgency
- Add public comments and private technician notes
- Save resolution summaries
- Automatically generate ticket references like `HD-2026-0001`
- Track status history
- Detect overdue tickets

### IT Asset Tracking

- Register laptops, desktops, printers, network devices, phones, and other assets
- Track asset tag, serial number, location, owner, and warranty date
- Link support tickets to affected assets
- Mark assets as active, in repair, retired, lost, or spare

### Dashboard and Reporting

- Dashboard summary cards
- Recent ticket list
- Overdue ticket count
- Tickets grouped by status and priority
- Search and filter tickets
- Export ticket data to CSV

### Demo data

A seed command creates realistic demo users, devices, and tickets so reviewers can test the project quickly.

## Tech stack

- Python 3
- Django 5
- SQLite
- HTML
- CSS
- JavaScript
- Docker optional
- GitHub Actions workflow included

## Project structure

```text
campus-it-helpdesk-portal/
├── apps/
│   ├── accounts/          # user profiles and roles
│   ├── assets/            # device / IT asset inventory
│   └── tickets/           # tickets, comments, status history, services
├── config/                # Django settings and root URLs
├── docs/                  # architecture, setup, test plan, resume text
├── sample_data/           # CSV templates and example data
├── scripts/               # helper scripts for setup
├── static/                # CSS and JS
├── templates/             # HTML templates
├── screenshots/           # add your own screenshots before publishing
├── Dockerfile
├── docker-compose.yml
├── manage.py
└── README.md
```

## Demo accounts

After running the seed command:

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `admin12345` |
| Technician | `technician1` | `tech12345` |
| Technician | `technician2` | `tech12345` |
| Requester | `student1` | `user12345` |
| Requester | `staff1` | `user12345` |

## Quick start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/campus-it-helpdesk-portal.git
cd campus-it-helpdesk-portal
```

### 2. Create and activate virtual environment

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Load demo data

```bash
python manage.py seed_helpdesk
```

### 6. Run the server

```bash
python manage.py runserver
```

Open this in your browser:

```text
http://127.0.0.1:8000/
```

## Optional Docker setup

```bash
docker compose up --build
```

Then open:

```text
http://127.0.0.1:8000/
```

## Testing

```bash
python manage.py test
```

## Suggested screenshots to add before publishing

Add real screenshots into the `screenshots/` folder:

1. Dashboard page
2. Ticket list with filters
3. Ticket detail page with comments
4. Asset list page
5. CSV export file opened in Excel

Then update this section with image links.

## Resume version

**Campus IT Helpdesk Portal**  
Technologies: Python, Django, SQLite, HTML, CSS, JavaScript

Developed a Django-based IT helpdesk portal for managing support tickets, technician assignments, troubleshooting notes, and IT assets. Implemented user authentication, role-based support workflows, ticket priorities, status history, asset linking, dashboard metrics, search/filtering, overdue ticket detection, and CSV export. Created realistic demo data, documentation, and tests to present the project as a professional GitHub portfolio item for IT support and junior IT specialist roles.

## Future improvements

- Email notifications when a ticket is assigned
- File attachments for screenshots
- SLA policy management from the admin panel
- Technician performance reports
- REST API using Django REST Framework
- Deployment to Render, Railway, or PythonAnywhere

## License

MIT License. You can use and modify this project for learning and portfolio purposes.
