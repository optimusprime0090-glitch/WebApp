"""
Project-level URL configuration for Employee_management.

This is the ROOT urlconf — Django reads this file for every single request.
It delegates to app-level urlconfs using include().

include('employees.urls') means:
  - Open employees/urls.py
  - Try each pattern in that file against the REMAINING URL path
  - If matched, hand the request to that view

The empty string prefix '' means employees app URLs are mounted at the site root.
So /employees/ works directly, not at /something/employees/.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django Admin — keep this; it's your administration interface
    path('admin/', admin.site.urls),

    # Delegate all other URLs to the employees app's url configuration.
    # '' prefix = no URL prefix added, so /employees/ maps directly.
    path('', include('employees.urls')),
]
