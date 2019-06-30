"""
WSGI config for Nflm_latest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import os, sys
import django
# django.setup()

sys.path.append('/home/ubuntu/Nflm_latest/Nflm_latest')

# add the virtualenv site-packages path to the sys.path
# sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Nflm_latest.settings")
# django.setup()

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Nflm_latest.settings")

application = get_wsgi_application()
