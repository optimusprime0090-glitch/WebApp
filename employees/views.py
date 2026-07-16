"""
views.py — Handles all HTTP requests for the employees app.

Each view function:
  - Receives an HttpRequest object
  - Interacts with the Employee model via Django ORM (no raw SQL)
  - Returns an HttpResponse (rendered template or redirect)

CRUD map:
  home             GET  /                          → dashboard with stats
  employee_list    GET  /employees/                → table of all employees
  employee_create  GET  /employees/create/         → blank form
                   POST /employees/create/         → validate + save + redirect
  employee_update  GET  /employees/<pk>/update/    → pre-filled form
                   POST /employees/<pk>/update/    → validate + save + redirect
  employee_delete  GET  /employees/<pk>/delete/    → confirmation page
                   POST /employees/<pk>/delete/    → delete record + redirect
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # one-time flash notifications
from .models import Employee
from .forms import EmployeeForm


# ---------------------------------------------------------------------------
# HOME — Dashboard
# ---------------------------------------------------------------------------

def home(request):
    """
    Renders the home/dashboard page at URL: /

    Queries a few aggregate statistics to display on the dashboard.
    Django ORM methods used:
      - .count()          → SELECT COUNT(*) FROM employees_employee
      - .order_by()[-3:]  → fetch last 3 added employees (by primary key)
    """
    # Total number of employees in the database
    total_employees = Employee.objects.count()

    # Count of distinct departments
    # .values('department') groups rows by department
    # .distinct() removes duplicates
    total_departments = Employee.objects.values('department').distinct().count()

    # The 3 most recently added employees (highest pk = newest)
    recent_employees = Employee.objects.order_by('-id')[:3]

    context = {
        'total_employees': total_employees,
        'total_departments': total_departments,
        'recent_employees': recent_employees,
    }
    return render(request, 'employees/home.html', context)


# ---------------------------------------------------------------------------
# READ — Employee List
# ---------------------------------------------------------------------------

def employee_list(request):
    """
    Displays all employees in a sortable table.
    URL: GET /employees/

    .all() fetches every row: SELECT * FROM employees_employee
    .order_by('name') sorts alphabetically by name.
    The queryset is lazy — it only hits the database when the template
    iterates over it with {% for employee in employees %}.
    """
    employees = Employee.objects.all().order_by('name')

    context = {
        'employees': employees,
        'employee_count': employees.count(),
    }
    return render(request, 'employees/employee_list.html', context)


# ---------------------------------------------------------------------------
# CREATE — Add New Employee
# ---------------------------------------------------------------------------

def employee_create(request):
    """
    Shows a blank form on GET; validates and saves on POST.
    URL: GET/POST /employees/create/

    POST flow:
      1. EmployeeForm(request.POST) binds submitted data to the form
      2. form.is_valid() runs field-level validation:
           - name and department must not be blank (required by default)
           - salary must be a valid decimal
           - values must respect max_length from the model
      3. If valid: form.save() runs INSERT INTO employees_employee (...)
         commit=True (default) means it's saved immediately
      4. messages.success() stores a flash message in the session
      5. redirect() sends HTTP 302 to the list page
         → browser makes a fresh GET request (Post/Redirect/Get pattern)
         → prevents duplicate submission on browser refresh

    GET flow:
      - EmployeeForm() with no arguments creates an empty unbound form
      - render() passes it to the template for display
    """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()  # INSERT INTO DB
            messages.success(
                request,
                f'Employee "{employee.name}" was added successfully.'
            )
            return redirect('employee-list')  # name from urls.py
    else:
        form = EmployeeForm()  # blank form for GET request

    context = {
        'form': form,
        'form_title': 'Add New Employee',
        'button_label': 'Save Employee',
    }
    return render(request, 'employees/employee_form.html', context)


# ---------------------------------------------------------------------------
# UPDATE — Edit Existing Employee
# ---------------------------------------------------------------------------

def employee_update(request, pk):
    """
    Shows a pre-filled form on GET; validates and updates on POST.
    URL: GET/POST /employees/<pk>/update/

    The 'pk' argument comes from the URL pattern <int:pk>.
    Django captures it from the URL and passes it as a keyword argument.

    get_object_or_404:
      - Tries Employee.objects.get(pk=pk)
      - If the employee exists → returns the Employee instance
      - If not found → raises Http404 (clean 404 page, not a 500 crash)

    EmployeeForm(request.POST, instance=employee):
      - The 'instance' argument tells the form to UPDATE this specific record
        rather than INSERT a new one
      - form.save() runs UPDATE employees_employee SET ... WHERE id = pk
    """
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        # Bind POST data AND the existing instance
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()  # UPDATE in DB
            messages.success(
                request,
                f'Employee "{employee.name}" was updated successfully.'
            )
            return redirect('employee-list')
    else:
        # Pre-populate the form with the existing employee's data
        form = EmployeeForm(instance=employee)

    context = {
        'form': form,
        'form_title': f'Edit Employee — {employee.name}',
        'button_label': 'Update Employee',
        'employee': employee,  # passed so template can show the employee name
    }
    return render(request, 'employees/employee_form.html', context)


# ---------------------------------------------------------------------------
# DELETE — Remove Employee
# ---------------------------------------------------------------------------

def employee_delete(request, pk):
    """
    Shows a confirmation page on GET; deletes on POST.
    URL: GET/POST /employees/<pk>/delete/

    Why a confirmation page?
      DELETE is irreversible. A confirmation step prevents accidental deletion
      from a misclick. The GET request shows "Are you sure?" and only the
      POST (form submission) actually deletes.

    employee.delete():
      - Runs DELETE FROM employees_employee WHERE id = pk
      - Django ORM handles any cascading deletes automatically
    """
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == 'POST':
        name = employee.name   # capture name before deletion for the message
        employee.delete()      # DELETE FROM DB
        messages.success(
            request,
            f'Employee "{name}" was deleted successfully.'
        )
        return redirect('employee-list')

    # GET request — show confirmation page with employee details
    context = {
        'employee': employee,
    }
    return render(request, 'employees/employee_confirm_delete.html', context)
