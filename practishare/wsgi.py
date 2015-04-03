"""
WSGI config for practishare project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import os, sys,site

sys.path.insert(0, '/usr/local/alwaysdata/python/django/1.6.4/')
sys.path.insert(0, '/home/practishare/practishare')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "practishare.settings")
site.addsitedir("/home/practishare/.local")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

