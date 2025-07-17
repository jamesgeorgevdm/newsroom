FROM python:3.13-slim

WORKDIR /newsroom

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . /newsroom

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD ["sh", "-c", "\
    until mysqladmin ping -hdb --silent; do \
        echo 'Waiting for MySQL...'; \
        sleep 1; \
    done && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8000"]
