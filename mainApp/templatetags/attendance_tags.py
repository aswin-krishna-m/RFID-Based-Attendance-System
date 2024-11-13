from django import template

register = template.Library()

@register.simple_tag
def total_attendance(student_subjects):
    total_classes = 0
    attended_classes = 0
    for key, value in student_subjects.items():
        if value.endswith('%'):  # Expecting percentage format
            percentage = float(value.strip('%'))
            total_classes += 100  # Assuming each subject has 100 total classes
            attended_classes += percentage

    if total_classes > 0:
        return f"{(attended_classes / total_classes):.2f}%"  # Final percentage
    return "0%"
