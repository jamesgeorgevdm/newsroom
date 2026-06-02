# Newsroom App (Django)

A multi-role news publishing platform built with Django. This capstone project demonstrates full-stack backend development, secure REST APIs, containerization, automated publishing pipelines, editorial workflows, and professional documentation.

## Features
* **Role-Based Workflows:** Distinct permissions and custom dashboards for Readers, Journalists, and Editors.
* **Modern Newsroom UI:** Dynamic, responsive interface for articles, newsletters, and an editorial feedback loop.
* **Automated Pipelines:** Integrated background actions for automated email notifications and tweet dispatching upon article publication.
* **Secure REST API:** Token-based API architecture built via Django REST Framework.
* **Production Optimized:** Configured with WhiteNoise for efficient static file serving and Gunicorn as the WSGI server.
* **Containerized Deployment:** Entire ecosystem packaged with Docker & docker-compose for deterministic environments.

### Tech Stack
* **Backend Framework:** Django 5.2.3 & Django REST Framework 3.16.0
* **Databases Supported:** Production-ready configuration for PostgreSQL / MariaDB (via `dj-database-url`)
* **Deployment & WSGI:** Docker, Gunicorn 22.0, WhiteNoise

---

## Live Demo
Available at: [Newsroom Online](https://newsroomonline.onrender.com/)  
*(Note: Hosted on a free instance tier. If the link is idle, please allow 60–90 seconds for the server to spin up.)*

---

## Example .env File
To protect production secrets, this project utilizes environment variables. A template file called `.env.example` is included in the repository. This must be copied to a local `.env` file and populated before initializing the application.

*This file contains sensitive credentials and should never be committed to source control.*

---

## Setup Instructions

### Please input the following commands into your terminal:

```bash
git clone https://github.com/jamesgeorgevdm/newsroom.git
cd newsroom
cp .env.example .env

# Ensure DB_HOST=db is set in your .env file for Docker networking

```

### Please make sure Docker Desktop is running successfully before beginning Docker initialization:

```bash
docker compose up -d
```
#### On the very first run, the MySQL container requires ~20 seconds to initialize its internal engine. You may initially see a django.db.utils.OperationalError in the logs - this is expected.
#### If the server doesn't catch up automatically, simply run:

```bash
docker compose restart web
```
### Once the containers are running, execute these commands:

```bash
# Apply database migrations
docker compose exec web python manage.py migrate

# Collect static files (CSS/JS)
docker compose exec web python manage.py collectstatic --noinput

# Create your admin credentials
docker compose exec web python manage.py createsuperuser
```
## Access the project:
- Frontend: http://localhost:8000
- Admin Dashboard: http://localhost:8000/admin

## .gitignore Recommendations

```
.env
venv/
__pycache__/
*.pyc
*.log
```

---

## Documentation

Auto-generated Sphinx docs live in `/docs`.

```bash
cd docs
make html
open build/html/index.html
```

---


