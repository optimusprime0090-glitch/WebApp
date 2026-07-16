"""
WSGI config for Employee_management project.
Exposes the WSGI callable as a module-level variable named 'application'.
"""

import os
import sys

# Ensure the project root (folder containing Employee_management/) is in sys.path.
# On Azure App Service, Gunicorn may run from a different working directory,
# so we resolve the path relative to this file: wsgi.py is inside
# Employee_management/, so two levels up is the project root.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Employee_management.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
