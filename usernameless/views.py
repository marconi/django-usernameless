from django.contrib.sites.models import RequestSite
from django.contrib.sites.models import Site

from registration import signals
from registration.models import RegistrationProfile
from registration.backends.default.views import (
    RegistrationView as BaseRegistrationView)

from .forms import RegistrationForm


class RegistrationView(BaseRegistrationView):
    form_class = RegistrationForm

    def register(self, request, **cleaned_data):
        """ We override register since the old one still uses username. """
        name, email, password = (cleaned_data['name'],
                                 cleaned_data['email'],
                                 cleaned_data['password1'])
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(
            name, email, password, site)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user
