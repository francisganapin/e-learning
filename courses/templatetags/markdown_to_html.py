import markdown as md_lib
from django import template

register = template.Library()

@register.filter
def markdown(text):
    """Converts markdown text to HTML."""
    if not text: return ""
    # We use 'extra' for tables/headers and 'codehilite' for code blocks
    return md_lib.markdown(text, extensions=['extra', 'codehilite'])
