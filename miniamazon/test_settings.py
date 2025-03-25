"""
Django test settings for miniamazon project.
"""

from .settings import *  # Import all settings from the main settings file

# Use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Use in-memory database for faster tests
    }
}

# Turn off debug mode for faster tests
DEBUG = False

# Disable password hashers to speed up tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Reduce log messages during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
} 