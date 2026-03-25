import re
from django import template

register = template.Library()

@register.filter
def to_embed_url(url):
    """Converts a standard YouTube URL to an embed URL."""
    if not url: return ""
    reg_exp = r'^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*'
    match = re.search(reg_exp, url)
    if match and len(match.group(2)) == 11:
        return f"https://www.youtube.com/embed/{match.group(2)}"
    return url
