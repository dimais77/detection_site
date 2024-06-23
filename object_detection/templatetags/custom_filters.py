# detection_site/object_detection/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def to_percentage(value):
    try:
        return f"{int(float(value) * 100)}%"
    except (ValueError, TypeError):
        return value
