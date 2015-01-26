import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Google App Engine imports.
from google.appengine.ext.webapp import util

# Force Django to reload its settings.
from django.conf import settings

settings._target = None

import django.core.handlers.wsgi
import django.core.signals
import django.db
import django.dispatch

# Unregister the rollback event handler.
django.dispatch.Signal.disconnect(
	django.core.signals.got_request_exception,
	django.db._rollback_on_exception)

# Create a Django application for WSGI.
application = django.core.handlers.wsgi.WSGIHandler()
