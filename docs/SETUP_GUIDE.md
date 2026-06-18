# Setup Guide

## Local setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py seed_helpdesk
python manage.py runserver
```

## Common setup problems

### `python: command not found`

Use `python3` instead of `python` on macOS/Linux.

### Port already in use

Run the server on a different port:

```bash
python manage.py runserver 8001
```

### Database looks empty

Run:

```bash
python manage.py seed_helpdesk
```
