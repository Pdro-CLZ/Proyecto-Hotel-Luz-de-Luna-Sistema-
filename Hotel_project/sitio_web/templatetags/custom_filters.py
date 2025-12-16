from django import template
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


from django.templatetags.static import static
from django.conf import settings


@register.filter
def img_url(value):
    """Return a usable URL for an image value.

    - If `value` is an absolute URL (starts with http:// or https://) return it unchanged.
    - Otherwise use Django's `static()` to build the URL from a static-relative path.
    """
    if not value:
        return ''
    try:
        v = str(value)
        if v.startswith('http://') or v.startswith('https://'):
            return v
        return static(v)
    except Exception:
        return value
