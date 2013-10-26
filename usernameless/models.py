"""
Patches for the registration.models.RegistrationManager methods.
"""

import hashlib
import random
import warnings
from autoslug import AutoSlugField

from django.db import transaction
from django.utils import timezone
from django.contrib.gis.db import models
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin,
                                        SiteProfileNotAvailable)


class UserManager(BaseUserManager):
    def create_user(self, name, email, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not name:
            msg = "Users must have a name"
            raise ValueError(msg)

        if not email:
            msg = "Users must have an email address"
            raise ValueError(msg)

        user = self.model(name=name, email=UserManager.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password):
        """
        Creates and saves a superuser with the given email, name and password.
        """
        user = self.create_user(name=name, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name=u'email address',
                              max_length=255,
                              unique=True,
                              db_index=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    slug = AutoSlugField(populate_from='name', unique=True)

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.slug)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
            PendingDeprecationWarning)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                    self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache

    def __unicode__(self):
        return self.email


@transaction.commit_on_success
def create_inactive_user(self, name, email, password, site, send_email=True):
    new_user = User.objects.create_user(name, email, password)
    new_user.is_active = False
    new_user.save()

    registration_profile = self.create_profile(new_user)

    if send_email:
        registration_profile.send_activation_email(site)

    return new_user


def create_profile(self, user):
    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(salt+user.email).hexdigest()
    return self.create(user=user, activation_key=activation_key)
