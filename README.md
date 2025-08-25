# SentiWise — Personal Finance Tracker

A simple Django web app to track income, expenses and budgets.  
This README explains the project purpose, core features, and how to run the project using the provided dependency list.

---

## What is SentiWise
SentiWise is a beginner-friendly personal finance tracker built with Django. It provides:
- Transaction tracking (income / expense)
- Categories and budgets
- A dashboard and transaction list with filtering and lazy-load on demand
- Minimal UI using Bootstrap + Crispy Forms

---

## Key features (so far)
- Transaction model with categories and user relations
- Category defaults for common income/expense types
- Dashboard and transactions list
- Filtering of transactions by type/category
- "Load more" lazy-loading for transaction lists (AJAX / on-demand)
- Static asset handling for images, SVGs and fonts (dev via Django staticfiles)

---

## Prerequisites
- Python 3.11+ (3.13 tested in dev)
- Git (optional)
- OS: Windows, macOS, Linux

Dependencies are listed in: `src/new_requirements.txt`

---

## Quick start (any OS)

1. Clone repo (or open project folder)
   - git clone <repo-url> or open the project directory in your IDE

2. Create and activate a virtual environment
   - Windows (PowerShell):
     python -m venv venv
     .\venv\Scripts\Activate.ps1
   - Windows (cmd):
     python -m venv venv
     .\venv\Scripts\activate
   - macOS / Linux:
     python3 -m venv venv
     source venv/bin/activate

3. Install dependencies
   - pip install --upgrade pip
   - pip install -r src/new_requirements.txt

4. Apply migrations
   - python manage.py migrate

5. Create a superuser (optional)
   - python manage.py createsuperuser

6. Run the development server
   - python manage.py runserver
   - Open http://127.0.0.1:8000/ in a browser

---

## Static files & SVGs
- Static files are served from `src/static/` during development. Confirm `STATICFILES_DIRS` in settings points to the static folder (it does).
- If SVG logos or fonts render incorrectly:
  - Ensure font files exist under `src/static/fonts/` and return 200 (no 404).
  - For inline SVG use `{% include 'transactions/svg/<file>.svg' %}` and place the file under `src/transactions/templates/transactions/svg/`.
  - For external SVG use `<img src="{% static 'images/...svg' %}">` and ensure `curl -I http://127.0.0.1:8000/static/...svg` returns 200.
  - Avoid problematic filenames (spaces, parentheses) for static assets to prevent URL-encoding issues.

---

## Common commands
- Run server: python manage.py runserver
- Shell: python manage.py shell
- Create migrations: python manage.py makemigrations
- Apply migrations: python manage.py migrate
- Collect static (production): python manage.py collectstatic

---

## Project structure (important parts)
- src/transactions/
  - models.py — Category, Transaction, Budget
  - views.py — dashboard & transaction views
  - templates/transactions/ — index.html, list_transaction.html, partials
- src/static/ — CSS, fonts, images, svgs
- src/new_requirements.txt — Python dependencies for the project

---

## Troubleshooting tips
- TemplateDoesNotExist for an SVG include: either move the SVG into `templates/…` or use `{% static %}` with the file in `static/`.
- 404 on font files: confirm file path under `src/static/fonts/` and test with curl or DevTools Network.
- JS not running: check browser console for HTML syntax errors (unclosed tags can stop scripts).
- If changes not visible, hard refresh the browser (Ctrl+F5) and restart the Django dev server.

---
## Virtual enviroment tips

## Beginner

Use a virtual environment to keep project dependencies isolated.

- Linux / macOS
  ```bash
  # create venv
  python3 -m venv venv

  # activate
  source venv/bin/activate

  # upgrade pip and install requirements
  python -m pip install --upgrade pip
  pip install -r src/new_requirements.txt
  ```

- Windows (PowerShell)
# create venv
python -m venv venv

# activate (PowerShell)
.\venv\Scripts\Activate.ps1

# upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r src/new_requirements.txt

- Windows (cmd.exe)
# create venv
python -m venv venv

# activate (cmd)
.\venv\Scripts\activate

# upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r src/new_requirements.txt

# To stop using virtual enviroment
deactivate

# Rest of project setup:
python manage.py migrate
python manage.py runserver