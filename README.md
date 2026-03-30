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

### Using docker-compose (Recommended)

```bash
# 0. Create .env from template 
cp .env.example .env

# 1. Build & start services in the background
docker-compose up --build -d

# 2. Create database tables (CRITICAL STEP)
docker-compose exec web python manage.py migrate

# 3. Create an admin account to test editorial roles
docker-compose exec web python manage.py createsuperuser

# 4. Open in browser:
#    http://localhost:8000

---
```

## Local Setup (venv)

```bash
# 1. Clone & enter project
git clone https://github.com/jamesgeorgevdm/newsroom.git
cd newsroom

# 2. Create & activate virtualenv
python -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Create your .env file and copy the contents of .env.example

# 5. Apply migrations & collect static files
python manage.py migrate
python manage.py collectstatic --noinput

# 6. Run the development server
python manage.py runserver

# 7. Open in browser
#    http://localhost:8000
```

---

## Docker Setup

### Manual Containers

```bash
# 1. Start MariaDB container
docker run -d \
  --name newsroom-db \
  -e MYSQL_ROOT_PASSWORD=your_password \
  -e MYSQL_DATABASE=newsroom \
  -e MYSQL_USER=newsuser \
  -e MYSQL_PASSWORD=newspassword \
  mariadb:latest

Ensure the environment variables (`MYSQL_*`, `DJANGO_*`, etc.) match those in your `.env` file

# 2. Build Django image
docker build -t jamesgeorgevdm/newsroom .

# 3. Run Django container linked to the DB
docker run -d \
  -p 8000:8000 \
  --name newsroom \
  --link newsroom-db:db \
  -e SECRET_KEY=your_secret_key \
  -e DEBUG=True \
  -e DJANGO_ALLOWED_HOST=localhost \
  -e MYSQL_DATABASE=newsroom \
  -e MYSQL_USER=newsuser \
  -e MYSQL_PASSWORD=newspassword \
  -e MYSQL_HOST=db \
  -e MYSQL_PORT=3306 \
  your-dockerhub-username/newsroom:latest

# 4. Open in browser:
#    http://localhost:8000
```

### Using docker-compose

```bash
# 1. Build & start services in the background
docker-compose up --build -d

# 2. Create database tables (CRITICAL STEP)
docker-compose exec web python manage.py migrate

# 3. Create an admin account to test editorial roles
docker-compose exec web python manage.py createsuperuser

# 4. Open in browser:
#    http://localhost:8000

---
```

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

## Git Branch Workflow

- `main` – Production-ready code  
- `container` – Docker tweaks  
- `docs` – Sphinx documentation

```bash
git branch
git branch --merged
```

---

## External Links

- Docker Hub: [https://hub.docker.com/r/your-dockerhub-username/newsroom](https://hub.docker.com/r/your-dockerhub-username/newsroom)  
- GitHub Repo: [https://github.com/yourusername/newsroom](https://github.com/yourusername/newsroom)
