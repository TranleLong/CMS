"""
ASGI config for Group9_CMS project.

It exposes quanlythe ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Group9_CMS.settings')

application = get_asgi_application()
