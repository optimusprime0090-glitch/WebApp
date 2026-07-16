FROM python:3.13-slim

WORKDIR /app

# Install ODBC Driver 18 for SQL Server (modern keyring approach for Debian 12/13)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gnupg2 unixodbc-dev \
    && curl -fsSL https://packages.microsoft.com/keys/microsoft.asc \
       | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-prod.gpg] https://packages.microsoft.com/debian/12/prod bookworm main" \
       > /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update \
    && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql18 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN DJANGO_SECRET_KEY=build-only \
    DJANGO_DEBUG=False \
    DJANGO_ALLOWED_HOSTS=localhost \
    DB_NAME=x DB_USER=x DB_PASSWORD=x DB_HOST=x DB_PORT=1433 \
    python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", \
     "--access-logfile", "-", "--error-logfile", "-", \
     "Employee_management.wsgi:application"]
