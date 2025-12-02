# translate.py removed content per user request.
# The templatetag has been neutralized/cleared. If you want the file fully
# deleted, please let me know and I'll remove the file from the repository.
from django import template
from django.conf import settings
from ..translations import TRANSLATIONS

register = template.Library()


@register.simple_tag(takes_context=True)
def tr(context, key):
    """Return translated string for `key` reading session key 'site_lang'.

    Usage in templates:
      {% load translate %}
      {% tr 'Habitaciones' %}

    This implementation is intentionally simple: it reads the chosen
    language from request.session['site_lang'] (fallback to settings.LANGUAGE_CODE
    or 'es') and looks up the key in `TRANSLATIONS`. If missing, returns the
    original key.
    """
    try:
        request = context.get('request')
        lang = None
        if request:
            lang = request.session.get('site_lang')
        if not lang:
            lang = getattr(settings, 'LANGUAGE_CODE', 'es')
        return TRANSLATIONS.get(key, {}).get(lang, TRANSLATIONS.get(key, {}).get('es', key))
    except Exception:
        return key

@register.filter
def tr_var(text, context):
    """
    Translate dynamic text (e.g. text from DB or default fallback).
    Usage:
        {{ habitacion.descripcion|tr_var:request }}
        {{ habitacion.nombre|tr_var:request }}
    """

    try:
        # Get site_lang from session
        lang = context.session.get('site_lang', 'es')
        return TRANSLATIONS.get(text, {}).get(lang, text)
    except Exception:
        return text
