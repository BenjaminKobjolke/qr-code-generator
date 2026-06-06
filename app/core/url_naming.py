import re
from datetime import date

from app.config.constants import (
    DEFAULT_SCHEME,
    FILENAME_DATE_FORMAT,
    NON_ALNUM_PATTERN,
    PNG_EXTENSION,
    SCHEME_PATTERN,
    SLUG_FALLBACK,
    WWW_PREFIX,
)


def normalize_url(raw: str) -> str:
    """Trim and prepend the default scheme when none is present."""
    url = raw.strip()
    if not re.match(SCHEME_PATTERN, url):
        url = DEFAULT_SCHEME + url
    return url


def _slugify(url: str) -> str:
    text = url.strip().lower()
    text = re.sub(SCHEME_PATTERN, "", text)
    if text.startswith(WWW_PREFIX):
        text = text[len(WWW_PREFIX) :]
    slug = re.sub(NON_ALNUM_PATTERN, "_", text).strip("_")
    return slug or SLUG_FALLBACK


def build_filename(url: str, today: date) -> str:
    """Return 'YYYY_MM_DD_<slug>.png' for the given url and date."""
    return f"{today.strftime(FILENAME_DATE_FORMAT)}_{_slugify(url)}{PNG_EXTENSION}"
