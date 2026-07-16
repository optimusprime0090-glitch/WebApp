"""
forms.py — Defines the HTML form for creating and editing Employee records.

We use ModelForm, which auto-generates form fields from the Employee model.
This means we don't repeat field definitions that already exist in models.py.

Flow when a user submits the form:
  1. Browser sends POST request with form data
  2. View creates EmployeeForm(request.POST) — binds the submitted data
  3. form.is_valid() runs all validation:
       - Are required fields present?
       - Is salary a valid decimal number?
       - Do values respect max_length constraints from the model?
  4. If valid: form.save() writes to the database via Django ORM
  5. If invalid: form is returned to the template with error messages attached
"""

from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    """
    A ModelForm for the Employee model.
    Handles both CREATE (no instance) and UPDATE (existing instance passed in).
    """

    class Meta:
        # Which model this form is based on
        model = Employee

        # Explicit field list — safer than '__all__'.
        # Only these three fields will appear in the rendered form.
        fields = ['name', 'department', 'salary']

        # Human-readable labels shown above each input field.
        # If omitted, Django auto-generates labels from field names
        # e.g. "name" → "Name", "salary" → "Salary"
        labels = {
            'name': 'Employee Name',
            'department': 'Department',
            'salary': 'Salary (₹)',
        }

        # widgets controls how each field is rendered as HTML.
        # We add Bootstrap's 'form-control' class and placeholder text
        # so the inputs look polished without extra CSS.
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name',
                'autofocus': True,          # cursor lands here when page loads
            }),
            'department': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Engineering, HR, Finance',
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'min': '0',                 # HTML5 client-side hint (not a security check)
                'step': '0.01',             # allows decimal input like 50000.50
            }),
        }

        # Help text appears below the field as a small hint.
        help_texts = {
            'salary': 'Enter the annual salary in INR.',
        }
