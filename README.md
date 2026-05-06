# Newsroom App (Django)

A multi-role news publishing platform built with Django. This capstone project demonstrates full-stack backend development, secure REST APIs, containerization, automated publishing, editorial workflows, and professional documentation.

---

## Features

- Modern newsroom-style interface for articles and newsletters  
- Role-based permissions (Readers, Journalists, Editors)  
- Automated tweets and email notifications on publish  
- Secure token-based API via Django REST Framework  
- Custom user model and editorial feedback loop  
- Containerized deployment with Docker & docker-compose  

---

## Example .env File

To protect secrets, this project includes a temporary file called `.env.example`, which contains example environment variables that must be copied into a `.env` file **before running the app**.  
This file should **not be committed to GitHub**, and exists only for evaluation purposes.

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


