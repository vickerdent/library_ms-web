"""
WSGI config for Library_MS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application

# Build paths inside the project like this: BASE_DIR / 'subdir'.
project_folder = os.path.expanduser('~/library_ms-web')
load_dotenv(os.path.join(project_folder, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Library_MS.settings')

application = get_wsgi_application()
