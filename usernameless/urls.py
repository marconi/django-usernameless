"""
An override to registration.backend.default.urls so we
can pass our custom RegistrationView with a custom form.
"""

from django.conf.urls import url

from registration.backends.default.urls import urlpatterns
from registration.auth_urls import urlpatterns as auth_urlpatterns

from .views import RegistrationView
from .forms import AuthenticationForm, PasswordResetForm, SetPasswordForm


# override the url for accounts/register
# with our custom RegistrationView.
urlpatterns[2] = url(
    r'^register/$',
    RegistrationView.as_view(),
    name='registration_register'
)

# remove relative resolution of auth_urls
# and instead concatenate auth_urls directly.
del urlpatterns[5]
urlpatterns += auth_urlpatterns

# override forms
urlpatterns[5].default_args.update({'authentication_form': AuthenticationForm})
urlpatterns[9].default_args.update({'password_reset_form': PasswordResetForm})
urlpatterns[10].default_args.update({'set_password_form': SetPasswordForm})
