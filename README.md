# Employee Management System

A production-ready Employee Management Web Application built with **Django 6**, **Azure SQL Database**, **Docker**, and deployed on **Azure App Service**.

**Live URL:** https://employeewebapp-shivam.azurewebsites.net

---

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Features](#features)
- [Local Development Setup](#local-development-setup)
- [Environment Variables](#environment-variables)
- [Docker Setup](#docker-setup)
- [Azure Deployment](#azure-deployment)
- [URL Routes](#url-routes)
- [Django MVT Pattern](#django-mvt-pattern)

---

## Project Overview

A full-stack web application to manage employees. Supports complete CRUD operations — Create, Read, Update, Delete — with a Bootstrap 5 responsive UI. The database backend is Azure SQL Server, managed entirely through Django ORM (no raw SQL).

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.13, Django 6.0.6 |
| Database | Azure SQL Server (mssql-django + pyodbc + ODBC Driver 18) |
| Frontend | Bootstrap 5.3, Bootstrap Icons |
| Static Files | WhiteNoise |
| WSGI Server | Gunicorn 26 |
| Container | Docker (python:3.13-slim) |
| Registry | Azure Container Registry (ACR) |
| Hosting | Azure App Service (Linux, B1) |
| Version Control | Git + GitHub |

---

## Architecture

```
Browser
   │
   ▼
Azure App Service (Linux)
   │
   ├── Docker Container
   │     ├── Gunicorn (WSGI server, port 8000)
   │     ├── Django Application
   │     │     ├── URLs → Views → Models → Templates
   │     │     └── WhiteNoise (static files)
   │     └── ODBC Driver 18
   │
   └── Azure SQL Database (EmployeeDB)
```

**Request Flow:**
```
Browser Request
  → App Service (HTTPS)
    → Gunicorn Worker
      → Django URL Router (urls.py)
        → View Function (views.py)
          → Django ORM (models.py)
            → Azure SQL Database
          ← QuerySet / Object
        ← Template Rendered (templates/)
      ← HTTP Response
    ← HTTP Response
  ← Page in Browser
```

---

## Project Structure

```
EmployeeWebApp/
│
├── Employee_management/          # Django project config
│   ├── settings.py               # All settings (env-var driven)
│   ├── urls.py                   # Root URL configuration
│   ├── wsgi.py                   # WSGI entry point for Gunicorn
│   └── asgi.py
│
├── employees/                    # Django app
│   ├── models.py                 # Employee model
│   ├── views.py                  # CRUD view functions
│   ├── urls.py                   # App-level URL patterns
│   ├── forms.py                  # EmployeeForm (ModelForm)
│   ├── admin.py                  # Django Admin registration
│   └── migrations/               # Database migrations
│
├── templates/                    # HTML templates
│   ├── base.html                 # Base layout (navbar, footer)
│   └── employees/
│       ├── home.html             # Dashboard
│       ├── employee_list.html    # Employee table
│       ├── employee_form.html    # Create / Edit form (shared)
│       └── employee_confirm_delete.html
│
├── static/
│   └── css/
│       └── style.css             # Custom CSS
│
├── Dockerfile                    # Docker image definition
├── .dockerignore                 # Files excluded from Docker build
├── .gitignore                    # Files excluded from Git
├── requirements.txt              # Python dependencies
└── manage.py                     # Django management CLI
```

---

## Features

- Dashboard with live stats (total employees, departments, recently added)
- Employee list with sortable table
- Add employee (Name, Department, Salary)
- Edit employee with pre-filled form
- Delete employee with confirmation page
- Flash messages for all actions (success/error)
- Responsive design — works on mobile and desktop
- Bootstrap 5 + Bootstrap Icons
- Post/Redirect/Get pattern to prevent duplicate form submissions
- CSRF protection on all forms
- WhiteNoise for static file serving (no separate CDN needed)

---

## Local Development Setup

### Prerequisites

- Python 3.13
- ODBC Driver 18 for SQL Server — [Install Guide](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Azure SQL Database (or SQL Server locally)

### Steps

**1. Clone the repository**
```bash
git clone https://github.com/optimusprime0090-glitch/WebApp.git
cd WebApp
```

**2. Create and activate virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create `.env` file in project root**
```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=EmployeeDB
DB_USER=your-sql-username
DB_PASSWORD=your-sql-password
DB_HOST=your-server.database.windows.net
DB_PORT=1433
```

**5. Run migrations**
```bash
python manage.py migrate
```

**6. Create superuser (for Django Admin)**
```bash
python manage.py createsuperuser
```

**7. Start development server**
```bash
python manage.py runserver
```

Open browser: http://127.0.0.1:8000

---

## Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DJANGO_SECRET_KEY` | Django secret key (required) | `your-secret-key` |
| `DJANGO_DEBUG` | Debug mode — `True` for local, `False` for prod | `False` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated allowed domains | `myapp.azurewebsites.net` |
| `DB_NAME` | Azure SQL database name | `EmployeeDB` |
| `DB_USER` | SQL Server admin username | `sqladmin` |
| `DB_PASSWORD` | SQL Server admin password | `Password@123` |
| `DB_HOST` | SQL Server hostname | `server.database.windows.net` |
| `DB_PORT` | SQL Server port (default 1433) | `1433` |

**Local:** Store in `.env` file (never commit this file)  
**Production:** Set in Azure App Service → Configuration → Application Settings

---

## Docker Setup

### Build image locally

```bash
docker build -t employeewebapp:latest .
```

### Run container locally

```bash
docker run -p 8000:8000 \
  -e DJANGO_SECRET_KEY=your-key \
  -e DJANGO_DEBUG=False \
  -e DJANGO_ALLOWED_HOSTS=localhost \
  -e DB_NAME=EmployeeDB \
  -e DB_USER=sqladmin \
  -e DB_PASSWORD=yourpassword \
  -e DB_HOST=server.database.windows.net \
  -e DB_PORT=1433 \
  employeewebapp:latest
```

Open browser: http://localhost:8000

---

## Azure Deployment

### Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed
- Docker Desktop installed
- Azure subscription

### Full deployment workflow

**1. Login to Azure**
```bash
az login
```

**2. Create Azure Container Registry (ACR)**
```bash
az acr create \
  --name employeewebappacr \
  --resource-group shivam-rg \
  --sku Basic \
  --admin-enabled true
```

**3. Login to ACR and build + push image**
```bash
az acr login --name employeewebappacr

docker build -t employeewebappacr.azurecr.io/employeewebapp:latest .

docker push employeewebappacr.azurecr.io/employeewebapp:latest
```

**4. Create App Service Plan (Linux B1)**
```bash
az appservice plan create \
  --name EmployeeAppPlan \
  --resource-group shivam-rg \
  --location centralindia \
  --sku B1 \
  --is-linux
```

**5. Create Web App**
```bash
az webapp create \
  --name employeewebapp-shivam \
  --resource-group shivam-rg \
  --plan EmployeeAppPlan \
  --deployment-container-image-name employeewebappacr.azurecr.io/employeewebapp:latest
```

**6. Configure Docker registry credentials**
```bash
# Get ACR password
ACR_PASSWORD=$(az acr credential show --name employeewebappacr --query "passwords[0].value" --output tsv)

az webapp config container set \
  --name employeewebapp-shivam \
  --resource-group shivam-rg \
  --docker-custom-image-name employeewebappacr.azurecr.io/employeewebapp:latest \
  --docker-registry-server-url https://employeewebappacr.azurecr.io \
  --docker-registry-server-user employeewebappacr \
  --docker-registry-server-password $ACR_PASSWORD
```

**7. Set environment variables**
```bash
az webapp config appsettings set \
  --name employeewebapp-shivam \
  --resource-group shivam-rg \
  --settings \
    DJANGO_SECRET_KEY="your-production-secret-key" \
    DJANGO_DEBUG="False" \
    DJANGO_ALLOWED_HOSTS="employeewebapp-shivam.azurewebsites.net" \
    DB_NAME="EmployeeDB" \
    DB_USER="sqladmin" \
    DB_PASSWORD="your-password" \
    DB_HOST="your-server.database.windows.net" \
    DB_PORT="1433" \
    WEBSITES_PORT="8000"
```

**8. Allow Azure services to access SQL Server**
```bash
az sql server firewall-rule create \
  --resource-group shivam-rg \
  --server your-sql-server \
  --name AllowAzureServices \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

**9. Restart and verify**
```bash
az webapp restart --name employeewebapp-shivam --resource-group shivam-rg
```

### Redeploy after code changes

```bash
# Rebuild and push new image
docker build -t employeewebappacr.azurecr.io/employeewebapp:latest .
docker push employeewebappacr.azurecr.io/employeewebapp:latest

# Restart App Service to pull new image
az webapp restart --name employeewebapp-shivam --resource-group shivam-rg
```

---

## URL Routes

| URL | Method | View | Description |
|---|---|---|---|
| `/` | GET | `home` | Dashboard with stats |
| `/employees/` | GET | `employee_list` | All employees table |
| `/employees/create/` | GET | `employee_create` | Blank add form |
| `/employees/create/` | POST | `employee_create` | Save new employee |
| `/employees/<id>/update/` | GET | `employee_update` | Pre-filled edit form |
| `/employees/<id>/update/` | POST | `employee_update` | Update employee |
| `/employees/<id>/delete/` | GET | `employee_delete` | Delete confirmation |
| `/employees/<id>/delete/` | POST | `employee_delete` | Delete employee |
| `/admin/` | GET | Django Admin | Admin interface |

---

## Django MVT Pattern

This project follows Django's **Model-View-Template** pattern:

```
Model (models.py)
  └── Employee class → maps to employees_employee table in Azure SQL
      Fields: name (CharField), department (CharField), salary (DecimalField)

View (views.py)
  └── Python functions that handle HTTP requests
      ├── Receive HttpRequest
      ├── Query Model via Django ORM
      └── Return HttpResponse (rendered template or redirect)

Template (templates/)
  └── HTML files with Django template tags
      ├── base.html         → shared layout
      └── employees/*.html  → page-specific content via {% extends %}

URL Router (urls.py)
  └── Maps URL patterns to View functions
      employees/urls.py  → app-level routes
      Employee_management/urls.py  → project-level, delegates via include()
```

---

## Key Design Decisions

**Why Docker instead of direct code deploy?**  
Azure App Service uses Oryx build system which sets its own PYTHONPATH. Docker gives full control over the Python environment — no path conflicts.

**Why WhiteNoise for static files?**  
Serves compressed static files directly from Gunicorn without needing a separate CDN or Nginx. Simple and production-ready.

**Why environment variables for all secrets?**  
`.env` for local dev, Azure App Service Application Settings for production. Same code, different sources — no secrets ever committed to Git.

**Why Post/Redirect/Get pattern?**  
After every successful POST (create/update/delete), the app redirects to a GET request. This prevents duplicate form submissions if the user refreshes the browser.
