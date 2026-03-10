"""
Utility helpers for the Artisan Dashboard application.
"""

from datetime import datetime


def format_timestamp(dt_string):
    """Format an ISO timestamp string into a human-readable format."""
    try:
        dt = datetime.fromisoformat(dt_string)
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except (ValueError, TypeError):
        return dt_string


def truncate_text(text, max_length=120):
    """Truncate text to a maximum length, adding ellipsis if needed."""
    if not text or len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "…"
