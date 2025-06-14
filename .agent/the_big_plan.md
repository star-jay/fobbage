Project Plan: Fobbage App Revitalization

This document outlines the plan to modernize the Fobbage quiz app with a new backend and React frontend, reduce hosting costs by migrating to Google Cloud, and address outstanding issues.
Pillar 0: Prep Work & Safety Net

Goal: Safely prepare for the refactor without losing any existing data or history.

Tasks:

    [ ] Backup Live Database (CRITICAL):

        Before any changes, perform a full backup of the live Heroku Postgres database. Download the backup file and store it securely.

    [ ] Create develop Branch:

        Create a new branch named develop from the master branch. This develop branch will be the base for the complete refactor, leaving master as a pristine copy of the original working version.

Pillar 1: Backend Refactor (The "Fresh Start")

Goal: Create a clean, modern, and simplified Django backend on the develop branch.

Tasks:

    [ ] Strip Down the Codebase:

        Delete all application code except for the Django models (models.py files). This preserves your database structure.

        Remove old views, templates, and unnecessary cruft.

    [ ] Modernize Dependencies:

        Switch the package manager from pip to uv.

        Create a new requirements.in file with only the essential packages (e.g., Django, psycopg2-binary for now, gunicorn).

        Run uv pip compile requirements.in > requirements.txt and uv pip sync to install.

    [ ] Remove Unneeded Services:

        Completely remove Daphne, channels, and any other websocket-related configurations.

    [ ] Validate Clean Backend:

        Ensure you can run the simplified Django project locally and that the database migrations work correctly.

Pillar 2: Modern Frontend with React

Goal: Build a new, responsive user interface as a single-page application using React.

Tasks:

    [ ] Setup Monolithic Structure:

        Set up a React project inside a frontend directory within your main Django project repository.

        Configure Django to serve the compiled React static files.

    [ ] Develop React Components:

        Plan and build the necessary React components for the quiz (e.g., QuestionDisplay, AnswerButtons, ScoreScreen).

    [ ] Build the API:

        Create a simple REST API using Django (e.g., with Django REST Framework or just Django views) that the React frontend will use to get questions and submit answers.

Pillar 3: Migration & Monolithic Deployment

Goal: Deploy the modernized monolithic application to a free-tier Google Cloud VM.

Tasks:

    [ ] Setup Google Cloud Environment:

        Create a Google Cloud account and set up a free-tier e2-micro Compute Engine VM in a US region.

    [ ] Configure the Server:

        Install uv, Python, Nginx, and Gunicorn on the VM.

        Configure Nginx to serve the static React files and proxy API requests to your Gunicorn/Django process.

    [ ] Deploy & Switch to SQLite:

        Transfer the refactored monolithic project to the VM.

        Final DB Switch: Change settings.py to use SQLite. Run manage.py migrate to create the final db.sqlite3 file on the server.

        (Optional) If you need to preserve data, write a one-time script to load the data from your Postgres backup into the new SQLite database.

    [ ] Go-Live & Decommission:

        Point your domain's DNS to the new VM's IP address.

        Thoroughly test the live application.

        Decommission the Heroku app and database to stop all charges.

Action Plan for Tonight's Session

Primary Goal: Complete the prep work and start the backend refactor.

    Safety First (30 mins):

        Person 1: Log in to Heroku and perform the database backup. This is the most important step.

        Person 2: Pull the latest from master and create the new develop branch.

    Backend Teardown (1-2 hours):

        Working together on the develop branch, start on Pillar 1.

        Begin by deleting old Django apps/code you know you don't need.

        Set up uv and try to get a minimal requirements.txt file working. The goal is to get manage.py runserver to work on a nearly empty project that only contains your models.