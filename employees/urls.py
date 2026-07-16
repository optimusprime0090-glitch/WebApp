"""
URL configuration for the employees app.

Each path() maps a URL pattern to a view function and assigns a name.
The name is used in templates with {% url 'name' %} so we never hardcode URLs.

These patterns are "mounted" under a prefix defined in the project urls.py.
Since the project mounts this at '', all these URLs are at the site root.
"""

from django.urls import path
from . import views  # import views from the same app (relative import)

urlpatterns = [
    # Home page — shows a welcome/dashboard page
    # URL: /
    path('', views.home, name='home'),

    # Employee list — shows all employees in a table
    # URL: /employees/
    path('employees/', views.employee_list, name='employee-list'),

    # Create employee — shows a blank form; on POST saves to DB
    # URL: /employees/create/
    path('employees/create/', views.employee_create, name='employee-create'),

    # Update employee — shows a pre-filled form for the given employee id
    # URL: /employees/5/update/
    # <int:pk> is a URL parameter — Django captures the integer and passes it
    # to the view as a keyword argument named 'pk' (primary key)
    path('employees/<int:pk>/update/', views.employee_update, name='employee-update'),

    # Delete employee — shows a confirmation page; on POST deletes the record
    # URL: /employees/5/delete/
    path('employees/<int:pk>/delete/', views.employee_delete, name='employee-delete'),
]
