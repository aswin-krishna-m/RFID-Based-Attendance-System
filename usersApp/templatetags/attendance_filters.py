# your_app/templatetags/attendance_filters.py

from django import template

register = template.Library()

@register.filter
def attendance_status(attendance_dict, student_id):
    """Return attendance status for a given student ID."""
    return attendance_dict.get(student_id, False)
