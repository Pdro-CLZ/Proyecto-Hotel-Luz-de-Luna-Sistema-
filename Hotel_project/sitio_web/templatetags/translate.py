# translate.py removed content per user request.
# The templatetag has been neutralized/cleared. If you want the file fully
# deleted, please let me know and I'll remove the file from the repository.
from django import template
from django.conf import settings
from ..translations import TRANSLATIONS
import os
from pathlib import Path
import re

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


@register.filter
def short_name(user):
    """Return short display name for a user: first token of first_name + first token of last_name.

    Usage in templates: {{ request.user|short_name }}
    Falls back to username if first/last name not available.
    """
    try:
        if not user:
            return ''
        first = getattr(user, 'first_name', '') or ''
        last = getattr(user, 'last_name', '') or ''
        first_token = first.strip().split()[0] if first.strip() else ''
        last_token = last.strip().split()[0] if last.strip() else ''
        if first_token and last_token:
            return f"{first_token} {last_token}"
        if first_token:
            return first_token
        if last_token:
            return last_token
        return getattr(user, 'username', '')
    except Exception:
        return getattr(user, 'username', '')


@register.simple_tag
def room_images(room_id):
    """Return a list of static-relative image paths for a given room id.

    Example return: ['sitio_web/images/Habitacion 1/IMG_0028.webp', ...]
    """
    try:
        base = Path(settings.BASE_DIR) / 'sitio_web' / 'static' / 'sitio_web' / 'images'
        target_folder = base / f'Habitacion {room_id}'

        allowed = {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif'}

        def list_images(folder: Path):
            if not folder.exists() or not folder.is_dir():
                return []
            return [p.name for p in sorted(folder.iterdir()) if p.is_file() and p.suffix.lower() in allowed]

        images = list_images(target_folder)

        # If no images for the exact folder, try to find the closest existing Habitacion N folder
        if not images:
            candidates = []
            for p in base.iterdir():
                if p.is_dir() and p.name.lower().startswith('habitacion'):
                    # try to extract a number
                    parts = p.name.split()
                    try:
                        num = int(parts[-1])
                        imglist = list_images(p)
                        if imglist:
                            candidates.append((num, p, imglist))
                    except Exception:
                        continue

            if candidates:
                # pick candidate with smallest absolute distance to requested id
                candidates.sort(key=lambda t: (abs(t[0] - int(room_id)), t[0]))
                chosen_num, chosen_folder, chosen_images = candidates[0]
                return [f"sitio_web/images/{chosen_folder.name}/{name}" for name in chosen_images]
        if images:
            return [f"sitio_web/images/Habitacion {room_id}/{name}" for name in images]

        # As a last resort, attempt to parse the detalle_habitacion template for hardcoded image URLs
        try:
            tpl_path = Path(settings.BASE_DIR) / 'sitio_web' / 'templates' / 'sitio_web' / f'detalle_habitacion_{room_id}.html'
            if tpl_path.exists():
                text = tpl_path.read_text(encoding='utf-8', errors='ignore')
                # Find all src attributes
                matches = re.findall(r'src=["\']([^"\']+)["\']', text)
                # keep only allowed extensions or absolute urls
                result = []
                for m in matches:
                    lower = m.lower()
                    if any(lower.endswith(ext) for ext in allowed) or lower.startswith('http://') or lower.startswith('https://'):
                        result.append(m)
                if result:
                    return result
        except Exception:
            pass

        return []
    except Exception:
        return []
