"""
Counter module for Healthy Bawarchi.

Tracks two simple numbers across all users:
  • Total visits  — page loads (deduplicated per session)
  • Recipes made  — successful recipe generations

Uses Abacus.Counter (https://abacus.jasoncameron.dev) — a free, no-signup
counter service. Numbers persist across deploys and are shared across all
users of this app.
"""

import requests
import time

# ─────────────────────────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────────────────────────

_BASE_URL        = "https://abacus.jasoncameron.dev"
NAMESPACE        = "healthy-bawarchi-original"
COUNTER_VISITS   = "visits"
COUNTER_RECIPES  = "recipes"

# Increased from 2.0 → 5.0 so cold-start wakeups don't time out
_TIMEOUT         = 5.0

# Retry up to 2 times before giving up
_MAX_RETRIES     = 2

# ─────────────────────────────────────────────────────────────────
# PUBLIC API
# ─────────────────────────────────────────────────────────────────

def record_visit() -> None:
    """Increment the visits counter. Call once per session."""
    _hit(COUNTER_VISITS)

def record_recipe() -> None:
    """Increment the recipes-generated counter. Call after each successful recipe."""
    _hit(COUNTER_RECIPES)

def get_counts() -> dict:
    """
    Return current counter values as a dict.
    Keys: 'visits', 'recipes'.
    On any failure, missing keys default to None — caller should handle.
    """
    return {
        "visits":  _get(COUNTER_VISITS),
        "recipes": _get(COUNTER_RECIPES),
    }

# ─────────────────────────────────────────────────────────────────
# INTERNAL
# ─────────────────────────────────────────────────────────────────

def _hit(counter_name: str):
    """Increment a counter by 1. Retries up to _MAX_RETRIES times. Fails silently."""
    url = f"{_BASE_URL}/hit/{NAMESPACE}/{counter_name}"
    for attempt in range(_MAX_RETRIES):
        try:
            r = requests.get(url, timeout=_TIMEOUT)
            if r.ok:
                return r.json().get("value")
        except Exception:
            if attempt < _MAX_RETRIES - 1:
                time.sleep(0.5)  # brief pause before retry
    return None

def _get(counter_name: str):
    """Return the current counter value without incrementing. Retries up to _MAX_RETRIES times."""
    url = f"{_BASE_URL}/get/{NAMESPACE}/{counter_name}"
    for attempt in range(_MAX_RETRIES):
        try:
            r = requests.get(url, timeout=_TIMEOUT)
            if r.ok:
                return r.json().get("value")
        except Exception:
            if attempt < _MAX_RETRIES - 1:
                time.sleep(0.5)  # brief pause before retry
    return None

def format_count(n) -> str:
    """
    Format a number for display: '1,247' instead of '1247'.
    Returns a placeholder dash if the count couldn't be fetched.
    """
    if n is None:
        return "—"
    try:
        return f"{int(n):,}"
    except Exception:
        return "—"
