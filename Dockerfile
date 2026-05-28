FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /newsroom

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    default-mysql-client \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY . /newsroom

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements-render.txt

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput && gunicorn newsroom.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]