# Newsroom App (Django)

A multi-role news publishing platform built with Django. This capstone project demonstrates full-stack backend development, containerization, automated publishing, editorial workflows, and professional documentation and deployment.

---

## Features

- **Modern News Presentation**  
  Articles and newsletters displayed in a polished newsroom-style interface

- **User Roles and Permissions**  
  - Readers: browse content, subscribe to journalists  
  - Journalists: write articles and send newsletters  
  - Editors: create publishers, approve content, or send back for feedback  
  - Groups and permissions automatically configured per role

- **Automated Communication**  
  - Tweets automatically posted when articles are published  
  - Emails sent to subscribed users for new content

- **Authentication and Recovery**  
  - Login, logout, and registration per user type  
  - Forgot password functionality included

- **Editorial Tools**  
  - Editors manage publisher entities and moderate journalist submissions  
  - Feedback loop for article revisions

- **Newsletter API**  
  Journalists can manage newsletters using Django REST Framework endpoints

- **Containerized Deployment**  
  Docker image built and published to Docker Hub  
  Runs on external environments including Docker Playground

---

## Local Setup with Virtual Environment

**Input the following commands:**

python -m venv venv
source venv/scripts/activate    
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver

## Docker Setup

**Pull and run the container**

docker pull jamesgeorgevdm/newsroom
docker run -p 8000:8000 --name newsroom jamesgeorgevdm/newsroom

**Apply database migrations inside container**

docker exec newsroom python manage.py migrate

Visit: http://localhost:8000 Click “Open Port” on Docker Playground to preview externally.

## Database Configuration

Please see the provided sensitive.txt file which has a pastable database configuration code. Paste this into settings.py. 


## Documentation
Documentation is auto-generated using Sphinx and lives in the /docs folder. Includes module docstrings and API references.

**To view locally:**

cd docs

open index.html  


Sphinx is configured to integrate with Django via conf.py:

python
import os, sys, django
sys.path.insert(0, os.path.abspath('..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'newsroom.settings'
django.setup()


## Git Branch Workflow

**Branches**

main - Final merged branch

container - Contains working Dockerfile

docs - Contains docstrings + Sphinx output

Both container and docs have been merged into master.

**Check branches and merge status:**

git branch

git branch --merged

## External Links


🐳 Docker Hub: jamesgeorgevdm/newsroom

🐙 GitHub Repo: https://github.com/jamesgeorgevdm/newsroom