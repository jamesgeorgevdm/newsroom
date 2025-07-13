# Use official Python base image
FROM python:3.13-slim

# Set working directory inside the container
WORKDIR /newsroom

# Copy everything into the container
COPY . /newsroom

# Install required system packages
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev libmariadb-dev pkg-config \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8000

# Start Django dev server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
