"""
Settings package for Django project.

Import the appropriate settings module based on the DJANGO_SETTINGS_MODULE environment variable.
Default to development settings if not specified.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Determine which settings to use
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .prod import *
else:
    from .dev import *
