# Add to your existing settings.py

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Add 'messaging' to INSTALLED_APPS
INSTALLED_APPS = [
    # ... other apps
    'messaging',
]