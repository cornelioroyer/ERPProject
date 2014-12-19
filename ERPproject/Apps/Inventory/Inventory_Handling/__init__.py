__author__ = 'Rhiyananta Catur Yudonegoro'

from django.conf import settings
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.management import create_superuser
from django.db.models import signals

settings.AUTO_CREATE_USER = getattr(settings, 'AUTO_CREATE_USER', True)

if settings.DEBUG and settings.AUTO_CREATE_USER:

    def create_testuser(app, created_models, verbosity, **kwargs):
        USERNAME = getattr(settings, 'AUTO_CREATE_USERNAME', 'admin')
        PASSWORD = getattr(settings, 'AUTO_CREATE_PASSWORD', '12345')
        EMAIL = getattr(settings, 'AUTO_CREATE_EMAIL', 'admin@admin.com')

        if getattr(settings, 'AUTO_CREATE_USER_CLASS', None):
            User = models.get_model(*settings.AUTO_CREATE_USER_CLASS.rsplit('.', 1))
        else:
            from django.contrib.auth.models import User

        try:
            User.objects.get(username=USERNAME)
        except User.DoesNotExist:
            if verbosity > 1:
                print '*' * 80
                print 'Creating test user -- login: %s, password: %s' % (USERNAME, PASSWORD)
                print '*' * 80
            assert User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        else:
            if verbosity > 1:
                print 'Test user already exists. -- login: %s, password: %s' % (USERNAME, PASSWORD)

    signals.post_syncdb.disconnect(
        create_superuser,
        sender=auth_models,
        dispatch_uid='django.contrib.auth.management.create_superuser')
    signals.post_syncdb.connect(create_testuser,
                                sender=auth_models, dispatch_uid='common.models.create_testuser')