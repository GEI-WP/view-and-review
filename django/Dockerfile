# BASE IMAGE
FROM python:3.10-slim AS base

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install python packages
RUN pip install poetry

# Set current working directory
WORKDIR /app/django

# Copy only requirements to cache them in docker layer
COPY poetry* pyproject* ./

# Project initialization
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy files
COPY . .

# Propagate changes in database schema
RUN python manage.py migrate --no-input

# Collect the static files into STATIC_ROOT (settings.py)
RUN python manage.py collectstatic --noinput --clear

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 1000 --disabled-password --gecos "" appuser && chown -R appuser .
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi"]